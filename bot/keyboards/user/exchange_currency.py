from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def output_all_possible_exchanges():

    from db.models.models import Partners

    keyboard = InlineKeyboardMarkup(inline_keyboard=[]) 

    # Получаем все доступные курсы валют и платформы
    all_currencies = []
    partners_info = await Partners.all()
    for info in partners_info:

        active_pairs = info.active_pairs
        for currencies in active_pairs:
            all_currencies.append([currencies.get('from', ''), currencies.get('platform', '')])
    

    # Получаем уникальные валюты и добавляем кнопки
    unique_data = [list(t) for t in set(tuple(sublist) for sublist in all_currencies)]
    for data in unique_data:
        button = InlineKeyboardButton(
            text=f'{data[0]} > {data[1]}',
            callback_data=f'type_exchange:{data[0].lower()}_{data[1].lower()}'
        )
        keyboard.inline_keyboard.append([button])


    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='🔙 Назад', callback_data='go_back_menu')
    ])

    return keyboard