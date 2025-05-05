async def display_available_exchanges():

    from db.models.models import Partners

    text = (
        'Поддерживаются обмены:\n\n'
    )

    # Получаем все доступные обмены
    all_currencies = []
    partners_info = await Partners.all()
    for info in partners_info:

        active_pairs = info.active_pairs
        for currencies in active_pairs:
            all_currencies.append([currencies.get('from', ''), currencies.get('to', '')])

    # Получаем уникальные строки в формате "XXX - YYY"
    unique_strings = set(f"{a} - {b}" for a, b in all_currencies)
    text += '\n'.join(unique_strings)
    text += '\n\nВыберите направление обмена'

    return text


async def partner_information(currency: str, platform: str, partner_id: int):

    from db.models.models import Partners, Exchanges, Rates

    partner_info = await Partners.get(tg_id=partner_id)
    count_exchanges = await Exchanges.get_deal_count_by_partner(partner_id)
    rate_info = await Rates.get(
        from_currency=currency,
        to_currency='CNY',
        platform=platform,
        partner_id=partner_id
    )

    text = (
        f'Выбран партнёр: {partner_info.name}\n'
        f'Совершенно обменов: {count_exchanges}\n'
        f'Курс: 1 CNY = {rate_info.rate} {currency}'
    )

    return text


async def confirmation_amount(currency: str, platform: str, partner_id: int):

    from db.models.models import Rates

    rate_info = await Rates.get(
        from_currency=currency,
        to_currency='CNY',
        platform=platform,
        partner_id=partner_id
    )

    return f'Введите сумму в CNY от {rate_info.limits}', rate_info.limits


incorrect_data = ['❗ Введите число, сумма которой положительная', '❗ Пожалуйста, введите корректную сумму числом', '❗ Пожалуйста, введите число в нужном диапазоне: ']


async def format_exchange_message(sum: float, currency: str, platform: str, partner_id: int) -> str:

    from db.models.models import Rates

    rate_info = await Rates.get(
        from_currency=currency,
        to_currency='CNY',
        platform=platform,
        partner_id=partner_id
    )

    cny_sum = round(sum/rate_info.rate)
    result = (
        f"\nВы отдаёте {sum} {currency.upper()}\n"
        f"для получения {cny_sum} CNY на {platform.capitalize()}\n"
    )

    return result
