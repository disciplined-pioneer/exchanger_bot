from settings import settings
from db.models.models import Exchanges

async def get_statistics_partners(partner_id: int) -> str:
    
    info_cny = await Exchanges.get_cny_sales_summary(partner_id=partner_id)
    commissions = await Exchanges.get_amout_to_current_month() * settings.bot.COMMISSION
    result = (
        "📆 Статистика обменов\n\n"
        f" - Продано CNY сегодня: {info_cny.get('day', 0.0)}\n"
        f" - Продано CNY за неделю: {info_cny.get('week', 0.0)}\n"
        f" - Продано CNY за месяц: {info_cny.get('month', 0.0)}\n\n"
        f"Комиссия к оплате: {commissions}"
    )

    return result