from db.models.models import ExchangeHistory

async def get_monthly_exchange_report() -> str:
    total_cny = await ExchangeHistory.get_cny_amount_current_month()
    rub_amount = await ExchangeHistory.get_currency_amount_for_month('RUB')
    usd_amount = await ExchangeHistory.get_currency_amount_for_month('USDT')

    return (
        "📆 Обменов за текущий месяц:\n\n"
        f"🇨🇳 CNY продано: {total_cny}\n"
        f"🇷🇺 RUB куплено: {rub_amount}\n"
        f"🇺🇸 USDT куплено: {usd_amount}"
    )
