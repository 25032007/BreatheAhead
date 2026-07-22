import pandas as pd
from prophet import Prophet
import numpy as np
import json

# Load data
df = pd.read_csv('../data/vadodara_aqi_history.csv')
df['date'] = pd.to_datetime(df['date'])

# Prophet needs columns named 'ds' and 'y'
prophet_df = df.rename(columns={'date': 'ds', 'aqi': 'y'})[['ds', 'y']]

# Split: last 10 days as test set, rest as train
train = prophet_df.iloc[:-10]
test = prophet_df.iloc[-10:]

# Train Prophet model
model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=False)
model.fit(train)

# Forecast for the test period + next 3 days (72 hours ahead)
future = model.make_future_dataframe(periods=13, freq='D')  # 10 test days + 3 future days
forecast = model.predict(future)

# --- Evaluate against test set ---
forecast_test = forecast.set_index('ds').loc[test['ds']]['yhat']
actual_test = test.set_index('ds')['y']

rmse_model = np.sqrt(np.mean((forecast_test.values - actual_test.values) ** 2))

# Persistence baseline: tomorrow's AQI = today's AQI (shift by 1)
baseline_pred = actual_test.shift(1).bfill()
rmse_baseline = np.sqrt(np.mean((baseline_pred.values - actual_test.values) ** 2))

print(f"Model RMSE: {rmse_model:.2f}")
print(f"Baseline RMSE: {rmse_baseline:.2f}")
improvement = ((rmse_baseline - rmse_model) / rmse_baseline) * 100
print(f"Improvement: {improvement:.1f}%")

# --- Get next 72-hour forecast for the dashboard ---
future_only = forecast[forecast['ds'] > prophet_df['ds'].max()]

output = {
    "ward": "Sayajigunj",
    "timestamps": future_only['ds'].astype(str).tolist(),
    "forecast_aqi": future_only['yhat'].round(1).tolist(),
    "baseline_aqi": [float(actual_test.iloc[-1])] * len(future_only),  # flat baseline from last known value
    "rmse_model": round(rmse_model, 2),
    "rmse_baseline": round(rmse_baseline, 2)
}

with open('../data/forecast_output.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\nSaved forecast_output.json")
print(json.dumps(output, indent=2))

def simulate_intervention(base_forecast, reduction_pct):
    """
    Simulate the effect of reducing traffic/construction activity.
    Simplifying assumption for MVP: each 10% reduction in activity 
    lowers AQI by ~6% (based on general literature that traffic/construction 
    contribute significantly to urban PM levels).
    """
    aqi_reduction_factor = (reduction_pct / 10) * 0.06
    simulated = [round(val * (1 - aqi_reduction_factor), 1) for val in base_forecast]
    return simulated

# Example: simulate a 30% reduction in traffic/construction activity
simulated_forecast = simulate_intervention(output['forecast_aqi'], reduction_pct=30)

print(f"\nOriginal forecast: {output['forecast_aqi']}")
print(f"After 30% activity reduction: {simulated_forecast}")

# Add to the JSON output so Person B can use it directly
output['simulated_forecast_30pct'] = simulated_forecast

with open('../data/forecast_output.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\nUpdated forecast_output.json with simulator data")