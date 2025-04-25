from db.models.models import ExchangeRate

starting_user_message = (
    "Стартовый текст для пользователя"
)

starting_admin_message = (
    "Привет, админ!"
)

async def get_exchange_rate() -> str:

    result = await ExchangeRate.get(id=1)
    if not result:
        return "❌ Курс валюты не найден."

    return (
        "<b>💱 Курс валюты</b>\n\n"
        "Текущий курс:\n\n"
        f"• <b>{result.rub_alipay}</b> ₽ = 1 Alipay\n"
        f"• <b>{result.rub_wechat}</b> ₽ = 1 WeChat\n"
        f"• <b>{result.usd_alipay}</b> USDT = 1 Alipay\n"
        f"• <b>{result.usd_wechat}</b> USDT = 1 WeChat"
    )

