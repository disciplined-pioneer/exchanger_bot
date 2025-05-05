from db.models.models import Partners


async def display_available_exchanges():

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