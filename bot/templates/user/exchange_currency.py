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
