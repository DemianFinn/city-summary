import time

import requests


def get_json(url: str) -> dict:
    """Выполняет GET-запрос с тайм-аутом и повторными попытками."""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "1")
                if retry_after.isdigit() and attempt < 2:
                    time.sleep(int(retry_after))
                    continue

            if response.status_code in (500, 502, 503, 504) and attempt < 2:
                time.sleep(1)
                continue

            response.raise_for_status()
            data = response.json()

            if not isinstance(data, dict):
                raise TypeError("API вернул ответ не в формате JSON-объекта")

            return data

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt == 2:
                raise
            time.sleep(1)

    raise RuntimeError("Не удалось получить ответ от API")
