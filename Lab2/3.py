import pandas as pd
df = pd.read_csv('weather_data.txt')

highest_precipitation = df[df['actual_precipitation'] == df['actual_precipitation'].max()]
highest_precipitation_dates = list(highest_precipitation['date'])
print('Days with the highest actual precipitation:', highest_precipitation_dates)

july_2014 = df[df['date'].str.contains('2014-7')]
average_max_temp = july_2014['actual_max_temp'].mean()
print('Average actual max temp for July 2014:', round(average_max_temp,2))

record_max_temp = df[df['actual_max_temp'] == df['record_max_temp']]
record_max_temp_dates = list(record_max_temp['date'])
print('Days with actual max temp as record max temp:', record_max_temp_dates)

october_2014 = df[df['date'].str.contains('2014-10')]
total_rain = october_2014['actual_precipitation'].sum()
print('Total rainfall in October 2014:', round(total_rain,2), 'inches')

low_temp = df['actual_min_temp'] < 60
high_temp = df['actual_max_temp'] > 90
same_day = df[low_temp & high_temp]
same_day_dates = list(same_day['date'])
if len(same_day_dates) > 0:
    print('Days where actual low temperature is below 60°F and actual max temperature above 90°F:', same_day_dates)
else:
    print('No days where actual low temperature is below 60°F and actual max temperature above 90°F.')

