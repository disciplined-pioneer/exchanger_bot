from db.models.models import Partners
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Меню", callback_data="go_back_menu")]
    ]
)

async def currency_keyboard(partner_id: int):

    info_partner = await Partners.get(tg_id=partner_id)
    active_pairs = info_partner.active_pairs

    # Создаём клавиатуру с пустым inline_keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])  # Инициализируем пустой список

    for info in active_pairs:
        platform = info.get('platform', '')
        currency = info.get('from', '')
        callback_data = f'change_value_{platform}_{currency}'.lower()

        button = InlineKeyboardButton(text=f'{platform} > {currency}', callback_data=callback_data)
        keyboard.inline_keyboard.append([button])  # Добавляем кнопку в клавиатуру

    # Кнопка "Назад"
    button = InlineKeyboardButton(text=f'🔙 Назад', callback_data='go_back_menu')
    keyboard.inline_keyboard.append([button])

    return keyboard


create_offer_back_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="create_offer_go_back")]
    ]
)