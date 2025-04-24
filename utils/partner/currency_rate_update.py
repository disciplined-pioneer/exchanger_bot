from aiogram.fsm.state import StatesGroup, State

class UpdateRates(StatesGroup):
    current_index = State()
    values = State()


# Список нужных курсов
LIST_CURRENCIES = {
    "rub_alipay": "Введите актуальный курс для пары CNY = RUB (Alipay)",
    "rub_wechat": "Введите актуальный курс для пары CNY = RUB (WeChat)",
    "usd_alipay": "Введите актуальный курс для пары CNY = USDT (Alipay)",
    "usd_wechat": "Введите актуальный курс для пары CNY = USDT (WeChat)"
}