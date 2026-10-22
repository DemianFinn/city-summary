from clients.rates import get_rate
from clients.weather import get_weather
from processing.preprocessing import process_rate, process_weather


def build_city_summary(city: str, currency: str = "USD") -> dict:
    """Получает данные и собирает итоговую сводку."""
    weather = process_weather(get_weather(city))
    rate = process_rate(get_rate(currency))

    return {
        "city": city,
        "weather": weather,
        "rates": {
            "currency": currency.upper(),
            **rate,
        },
    }
