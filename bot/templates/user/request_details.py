from db.models.models import ExchangeRate, ExchangeHistory


# Выбор партнёра + курс
async def get_partner_summary_text(partner_id: str) -> str:
    
    result = await ExchangeRate.get(id=1)
    count_trade = await ExchangeHistory.get_deal_count_by_partner(int(partner_id))
    result = (  
        f"Вы выбрали партнёра №{partner_id}\n"
        f"Совершено обменов: {count_trade}\n\n"
        f"• <b>{result.rub_alipay}</b> ₽ = 1 Alipay\n"
        f"• <b>{result.rub_wechat}</b> ₽ = 1 WeChat\n"
        f"• <b>{result.usdt_alipay}</b> USDT = 1 Alipay\n"
        f"• <b>{result.usdt_wechat}</b> USDT = 1 WeChat"
    )
    return result


types_exchange_text = (
    "💱 <b>Поддерживается обмен:</b>\n\n"
    "• RUB → CNY\n"
    "• USDT → CNY\n\n"
    "🔽 Выберите направление обмена:"
)

async def format_exchange_message(sum: float, currency: str, platform: str) -> str:

    cny_sum = round(sum/await ExchangeRate.get_exchange_rate(f"{currency}_{platform}"))
    result = (
        f"\nВы отдаёте {sum} {currency.upper()}\n"
        f"для получения {round(cny_sum, 3)} CNY на {platform.capitalize()}\n"
    )

    return result


incorrect_data = ['❗ Сумма должна быть положительной. Введите число:', '❗ Пожалуйста, введите корректную сумму числом. Введите число:']

waiting_details = (
    "Ожидайте реквизиты для оплаты\n"
    "(здесь будут написаны условия пополнения)"
)

async def format_exchange_request(amount: float, currency: str) -> str:
    return (
        "Получение заявки на обмен:\n\n"
        f"Сумма: {amount}\n"
        f"Валюта: {currency.upper()}\n"
        f"Нажмите на кнопку ниже для продолжения ⬇️"
    )

