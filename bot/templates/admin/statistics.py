from db.models.models import Exchanges, Commissions

async def get_monthly_exchange_report() -> str:
    
    total_cny = await Exchanges.get_amout_to_current_month()
    total_rub = await Exchanges.get_amout_from_for_month("RUB")
    total_usdt = await Exchanges.get_amout_from_for_month("USDT")

    all_history_count = len(await Exchanges.all())
    sum_comissions = await Commissions.get_monthly_commission_sum()

    result = (
        "📆 Обменов за текущий месяц:\n\n"
        f"🇨🇳 CNY продано: {total_cny}\n"
        f"🇷🇺 RUB куплено: {total_rub}\n"
        f"🇺🇸 USDT куплено: {total_usdt}\n\n"
        f"Сделок проведено: {all_history_count}\n"
        f"На комиссиях заработано: {sum_comissions}"
    )

    return result
