# 1. импорты из стандартной библиотеки
import os
from typing import Dict, Optional

# 2. импорты сторонних библиотек
from dotenv import load_dotenv
import requests  # type: ignore
from requests.models import Response  # type: ignore

# 3. импорты модулей текущего проекта


load_dotenv()

GEO_KEY: Optional[str] | str = os.getenv('GEO_KEY')
GEO_URL: Optional[str] | str = os.getenv('GEO_API_URL')
YAW_API: Optional[str] | str = os.getenv('API_YA_WEATHER')
YAW_URL: Optional[str] | str = os.getenv('YA_WEATHER_URL')


def get_coordinates(place, geo_api: str, geo_url: str) -> str:
    payload: Dict[str, str] = {
        'apikey': geo_api,
        'geocode': place,
        'format': 'json'
    }
    try:
        resp: Response = requests.get(geo_url, params=payload)
    except requests.RequestException as error:
        print(f'Error arised: {error}')
    return (
        resp.json()['response']['GeoObjectCollection']['featureMember'][0]
        ['GeoObject']['Point']['pos']
    )


def get_weather_data(place: str, yaw_api=YAW_API, yaw_url=YAW_URL,
                     geo_api=GEO_KEY, geo_url=GEO_URL
                     ) -> Dict[str, str | float]:
    lon, lat = get_coordinates(place, geo_api, geo_url).split()
    headers: Dict[str, str] = {'X-Yandex-API-Key': yaw_api}
    payload: Dict[str, str] = {
        'lat': lat,
        'lon': lon,
        'lang': 'ru_RU'
    }
    try:
        resp: Response = requests.get(
            yaw_url, params=payload, headers=headers
            )
    except requests.RequestException as error:
        print(f'Error arised: {error}')
    return resp.json()['fact']
