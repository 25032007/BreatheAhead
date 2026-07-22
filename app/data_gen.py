import pandas as pd
import numpy as np

np.random.seed(7)
n = 60
dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq='D')
day_of_week = dates.dayofweek

# Strong weekday/weekend plateau pattern (weekdays: traffic+construction high, weekends: low)
weekly_pattern = np.where(day_of_week < 5, 150, 90)

# Slight upward trend (pollution build-up over the period)
trend = np.linspace(0, 10, n)

# Small noise relative to the weekly swing, so the pattern is learnable
noise = np.random.normal(0, 4, n)

aqi = weekly_pattern + trend + noise
aqi = np.clip(aqi, 40, 300)

df = pd.DataFrame({'date': dates, 'aqi': aqi})
df.to_csv('../data/vadodara_aqi_history.csv', index=False)
print(df.tail(10))
print("Regenerated data/vadodara_aqi_history.csv")

