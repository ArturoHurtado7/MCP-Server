from typing import Any, Dict, Optional, Tuple

import requests

GEOCODING_API_BASE_URL = "https://geocoding-api.open-meteo.com/v1"
WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1"

def get_city_coordinates(city_name: str) -> Optional[Tuple[float, float]]:
    """
    Obtiene las coordenadas (latitud, longitud) de una ciudad usando la API de Open-Meteo.

    Args:
        city_name (str): Nombre de la ciudad a buscar.

    Returns:
        Optional[Tuple[float, float]]: Una tupla con latitud y longitud si se encuentra la ciudad, de lo contrario None.
    """
    url = f"{GEOCODING_API_BASE_URL}/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results")
        if results and len(results) > 0:
            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            return (lat, lon)
    return None

def get_weather_forecast(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Obtiene el pronóstico del clima para una ubicación específica usando la API de Open-Meteo.

    Args:
        latitude (float): Latitud de la ubicación.
        longitude (float): Longitud de la ubicación.

    Returns:
        Optional[Dict[str, Any]]: Diccionario con la información del clima si la consulta es exitosa, de lo contrario None.
    """
    url = f"{WEATHER_API_BASE_URL}/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "current": "temperature_2m,precipitation,rain,is_day",
        "forecast_days": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None
