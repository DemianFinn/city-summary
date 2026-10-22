from clients.http import get_json


def get_weather(city: str) -> dict:
    """Получает текущую погоду для города через Open-Meteo."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_data = get_json(f"{geo_url}?name={city}&count=1&language=en&format=json")

    results = geo_data.get("results")
    if not results:
        raise LookupError(f"Город не найден: {city}")

    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_data = get_json(
        f"{weather_url}?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,weather_code"
    )

    current = weather_data.get("current")
    if not isinstance(current, dict):
        raise TypeError("В ответе погоды отсутствует поле current")

    temperature = current.get("temperature_2m")
    weather_code = current.get("weather_code")

    if not isinstance(temperature, (int, float)) or weather_code is None:
        raise ValueError("Некорректные данные о погоде")

    descriptions = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "depositing rime fog",
        51: "light drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        71: "slight snow",
        73: "moderate snow",
        75: "heavy snow",
        95: "thunderstorm",
    }

    return {
        "temp_c": float(temperature),
        "description": descriptions.get(weather_code, "unknown weather"),
    }
