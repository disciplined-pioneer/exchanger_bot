import re
from aiogram.fsm.state import StatesGroup, State

class CollectingCurrencyInfo(StatesGroup):
    start = ()
    range_limits = State()
    exchange_rate = State()


def validate_limits_input(text: str) -> tuple[bool, str | None]:
    """
    Проверяет, что ввод соответствует формату "100-500", оба числа > 0 и min < max.
    Возвращает (True, None) при успехе, иначе (False, сообщение об ошибке).
    """
    text = text.strip()
    match = re.fullmatch(r'([1-9]\d*)-([1-9]\d*)', text)

    if not match:
        return False, "❗️ Введите диапазон в формате 100-500. Оба числа должны быть положительными и больше нуля, без лишних символов и нулей в начале"

    min_val, max_val = map(int, match.groups())
    if min_val >= max_val:
        return False, "❗️ Минимум должен быть меньше максимума. Пример: 100-500"

    return True, None


def validate_exchange_rate(text: str) -> tuple[bool, str | None]:
    """
    Проверяет, что введённый курс — это положительное число.
    Возвращает (True, None) при успехе, иначе (False, текст ошибки).
    """
    text = text.strip().replace(",", ".")  # заменяем запятую на точку

    try:
        rate = float(text)
        if rate <= 0:
            return False, "❗️ Курс должен быть числом больше 0"
    except ValueError:
        return False, "❗️ Пожалуйста, введите корректное число, например: 12.5"

    return True, None
