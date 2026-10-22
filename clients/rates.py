import requests

from clients.http import get_json


def get_rate(currency: str) -> float:
    """Получает курс валюты к рублю через Frankfurter."""
    url = f"https://api.frankfurter.dev/v2/rate/{currency}/RUB"

    try:
        data = get_json(url)
    except requests.exceptions.HTTPError as error:
        if error.response is not None and error.response.status_code in (400, 404, 422):
            raise LookupError(f"Неизвестный код валюты: {currency}") from error
        raise

    rate = data.get("rate")
    if not isinstance(rate, (int, float)):
        raise TypeError(f"Некорректный ответ курса валюты: {currency}")

    return float(rate)
