from aiogram.fsm.state import State, StatesGroup
from db.models.models import ExchangeRate, ExchangeHistory


class ExchangeStates(StatesGroup):
    summ = State()


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

    cny_sum = await ExchangeRate.get_exchange_rate(f"{currency}_{platform}")
    result = (
        f"\nВы отдаёте {sum} {currency.upper()}\n"
        f"для получения {cny_sum} CNY на {platform.capitalize()}\n"
    )

    return result
