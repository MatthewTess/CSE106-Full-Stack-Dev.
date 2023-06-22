import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('weather_data.txt')



df.plot(x='date', y=['actual_max_temp', 'actual_min_temp'], color=['red', 'blue'])
plt.title('Actual Max and Min Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend(['Max Temp', 'Min Temp'])
plt.show()

df['actual_precipitation'].plot.hist(bins=10)
plt.title('Actual Precipitation')
plt.xlabel('Precipitation (in)')
plt.ylabel('Frequency')
plt.show()