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
        f"• <b>{result.usd_alipay}</b> USDT = 1 Alipay\n"
        f"• <b>{result.usd_wechat}</b> USDT = 1 WeChat"
    )
    return result


types_exchange_text = (
    "💱 <b>Поддерживается обмен:</b>\n\n"
    "• RUB → CNY\n"
    "• USDT → CNY\n\n"
    "🔽 Выберите направление обмена:"
)
