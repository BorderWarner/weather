import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def get_weather(forecast_days, latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "forecast_days": forecast_days,
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability",
                   "precipitation", "rain", "snowfall", "snow_depth", "pressure_msl", "cloud_cover", "wind_speed_10m",
                   "surface_pressure"],
        "timezone": "Europe/Moscow"
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
    hourly_rain = hourly.Variables(5).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(6).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(7).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(8).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(9).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(10).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(11).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "temperature_2m": hourly_temperature_2m, "relative_humidity_2m": hourly_relative_humidity_2m,
        "apparent_temperature": hourly_apparent_temperature,
        "precipitation_probability": hourly_precipitation_probability,
        "precipitation": hourly_precipitation, "rain": hourly_rain, "snowfall": hourly_snowfall,
        "snow_depth": hourly_snow_depth, "pressure_msl": hourly_pressure_msl, "cloud_cover": hourly_cloud_cover,
        "wind_speed_10m": hourly_wind_speed_10m, "surface_pressure": hourly_surface_pressure}

    return pd.DataFrame(data=hourly_data), response.Latitude(), response.Longitude(), response.Elevation()



