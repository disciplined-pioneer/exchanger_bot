from settings import settings
from db.models.models import Exchanges

async def get_statistics_partners(partner_id: int) -> str:
    
    info_cny = await Exchanges.get_cny_sales_summary(partner_id=partner_id)
    commissions = await Exchanges.get_partner_commission(partner_id)
    result = (
        "📆 Статистика обменов\n\n"
        f" - Сумма обменов за сегодня: {info_cny.get('day', 0.0)} CNY\n"
        f" - Сумма обменов за неделю: {info_cny.get('week', 0.0)} CNY\n"
        f" - Сумма обменов за месяц: {info_cny.get('month', 0.0)} CNY\n\n"
        f"Комиссия к оплате: {commissions} CNY"
    )

    return result