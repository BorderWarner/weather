from get_weather import get_weather
import pandas as pd

hourly_dataframe, latitude, longitude, elevation = get_weather(16, 55.710803, 37.473970)
print(f"Координаты: {latitude} с.ш. {longitude} в.д.")
print(f"Высота: {elevation} м")
# print(hourly_dataframe)

target_datetime = pd.to_datetime("2024-06-09 16:00:00", utc=True)

matching_row = hourly_dataframe[hourly_dataframe['date'] == target_datetime]

if not matching_row.empty:
    print('Температура: ', matching_row['temperature_2m'].values[0])
    print('Влажность: ', matching_row['relative_humidity_2m'].values[0])
    print('Скорость ветра: ', matching_row['wind_speed_10m'].values[0])
    print('Облачность: ', matching_row['cloud_cover'].values[0])
    print('Поверхностное давление: ', matching_row['surface_pressure'].values[0])
else:
    print("Нет данных")
