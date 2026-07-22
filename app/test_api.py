import pandas as pd
import numpy as np

dates = pd.date_range(end=pd.Timestamp.now(), periods=60, freq='D')
np.random.seed(42)
base = 130 + 30*np.sin(np.linspace(0, 6, 60))
noise = np.random.normal(0, 15, 60)
aqi = np.clip(base + noise, 40, 300)

df = pd.DataFrame({'date': dates, 'aqi': aqi})
df.to_csv('../data/vadodara_aqi_history.csv', index=False)
print(df.tail())
print("Saved to data/vadodara_aqi_history.csv")