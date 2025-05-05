from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Кнопки со всеми видами обменов
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


# Кнопки со всеми объявлениями согласно парамметрам
async def buttons_with_all_ads(currency: str, platform: str):

    from db.models.models import Partners, Rates

    keyboard = InlineKeyboardMarkup(inline_keyboard=[]) 
    list_ids = await Partners.get_ids_by_from_and_platform(currency, platform)

    for tg_id in list_ids:
        rate = await Rates.get_latest_rate(
            from_currency=currency,
            to_currency='CNY',
            platform=platform,
            partner_id=tg_id
        )

        if rate is None:
            continue  # Пропускаем, если нет курса

        info_partner = await Partners.get(tg_id=tg_id)
        if info_partner is None:
            continue  # Пропускаем, если нет партнёра

        button = InlineKeyboardButton(
            text=f'{rate.rate} {currency} ({rate.limits}) - {info_partner.name}',
            callback_data=f'partner_id:{tg_id}'
        )
        keyboard.inline_keyboard.append([button])


    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='🔙 Назад', callback_data='go_back_exchange:exchange_currency')
    ])

    return keyboard


async def keyboard_exchange_confirm(currency: str, platform: str):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💱 Совершить обмен", callback_data="start_confirm_exchange")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"go_back_exchange:type_exchange:{currency}_{platform}")]
        ]
    )

    return keyboard


back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Меню', callback_data='go_back_menu')]
    ]
)

confirm_cancel_exchange = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ Верно, начать обмен', callback_data='confirm_exchange')],
        [InlineKeyboardButton(text='❌ Отменить обмен', callback_data='go_back_menu')]
    ]
)
