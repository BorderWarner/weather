from get_weather import get_weather
import pandas as pd

hourly_dataframe, latitude, longitude, elevation = get_weather(16, 56.062435, 159.903470)
print(f"Координаты: {latitude} с.ш. {longitude} в.д.")
print(f"Высота: {elevation} м")
# print(hourly_dataframe)

target_datetime = pd.to_datetime("2024-06-08 22:00:00", utc=True)

matching_row = hourly_dataframe[hourly_dataframe['date'] == target_datetime]

if not matching_row.empty:
    print(matching_row['temperature_2m'].values[0])
else:
    print("Нет данных")
