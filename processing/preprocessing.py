def process_weather(weather: dict) -> dict:
    """Добавляет флаг необходимости тёплой одежды."""
    result = weather.copy()
    result["warm_clothes"] = result["temp_c"] < 0

    if not result.get("description"):
        result["description"] = "description unavailable"

    return result


def process_rate(rate: float) -> dict:
    """Добавляет флаг дорогого курса."""
    return {
        "rate_to_rub": rate,
        "expensive": rate > 100,
    }
