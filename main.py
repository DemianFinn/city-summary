import argparse
import sys

import requests

from processing.service import build_city_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Сводка погоды и курса валют")
    parser.add_argument("--city", required=True, help="Название города")
    parser.add_argument(
        "--currency", default="USD", help="Код валюты, например USD или EUR"
    )
    args = parser.parse_args()

    currency = args.currency.upper()

    try:
        summary = build_city_summary(args.city, currency)
    except LookupError as error:
        print(f"Не найден город или код валюты: {error}", file=sys.stderr)
        return 3
    except requests.exceptions.RequestException as error:
        print(f"Внешний сервис недоступен: {error}", file=sys.stderr)
        return 4
    except (ValueError, KeyError, TypeError) as error:
        print(f"Некорректный ответ внешнего сервиса: {error}", file=sys.stderr)
        return 4

    weather = summary["weather"]
    rates = summary["rates"]

    print(f"Город: {summary['city']}")
    print(f"Погода: {weather['temp_c']}°C, {weather['description']}")
    print(f"Тёплая одежда: {'да' if weather['warm_clothes'] else 'нет'}")
    print(f"{rates['currency']}→RUB: {rates['rate_to_rub']:.2f}")
    print(f"Дорогой курс: {'да' if rates['expensive'] else 'нет'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
