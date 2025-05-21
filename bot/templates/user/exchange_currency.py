async def display_available_exchanges():

    from db.models.models import Partners

    text = (
        'Поддерживаются обмены:\n\n'
    )

    # Получаем все доступные обмены
    all_currencies = []
    partners_info = await Partners.all()

    # Если нет партнёров - нет обменов
    if not partners_info:
        text = '❕ В данный момент обменов нет!'
        return text
    
    # Добавляемм обмены
    for info in partners_info:
        active_pairs = info.active_pairs
        for currencies in active_pairs:
            all_currencies.append([currencies.get('from', ''), currencies.get('to', '')])

    # Получаем уникальные строки в формате "XXX - YYY"
    unique_strings = set(f"{a} - {b}" for a, b in all_currencies)
    text += '\n'.join(unique_strings)
    text += '\n\nВыберите направление обмена'

    return text


async def partner_information(currency: str, id: int):

    from db.models.models import Partners, Exchanges, Rates

    rate_info = await Rates.get(id=id)
    partner_info = await Partners.get(tg_id=rate_info.partner_id)
    count_exchanges = await Exchanges.get_deal_count_by_partner(partner_id=rate_info.partner_id)

    text = (
        f'Выбран партнёр: {partner_info.name}\n'
        f'Совершенно обменов: {count_exchanges}\n'
        f'Курс: 1 CNY = {rate_info.rate} {currency}'
    )

    return text, rate_info.partner_id


async def confirmation_amount(currency: str, id: int):

    from db.models.models import Rates

    rate_info = await Rates.get(
        id=id
    )

    return f'Введите сумму в CNY диапазоне {rate_info.limits} {currency}', rate_info.limits


incorrect_data = ['❗ Введите число, сумма которой положительная', '❗ Пожалуйста, введите корректную сумму числом', '❗ Пожалуйста, введите число в нужном диапазоне: ']


async def format_exchange_message(sum: float, currency: str, platform: str, id: int) -> str:

    from db.models.models import Rates

    rate_info = await Rates.get(
        id=id
    )

    cny_sum = round(sum/rate_info.rate)
    result = (
        f"\nВы отдаёте {sum} {currency.upper()}\n"
        f"для получения {cny_sum} CNY на {platform.capitalize()}\n\n"
        'ВНИМАНИЕ, ТУТ ПРЕДУПРЕЖДЕНИЕ'
    )

    return result, cny_sum


async def format_exchange_request(amount: float, currency: str, platform: str) -> str:
    return (
        "Получение заявки на обмен:\n\n"
        f"Сумма: {amount}\n"
        f"Валюта: {currency.upper()}\n"
        f"Платформа: {platform}\n\n"
        f"Нажмите на кнопку ниже для продолжения ⬇️"
    )
