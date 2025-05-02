from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="go_back_menu")]
    ]
)

back_menu_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Меню", callback_data="go_back_menu")]
    ]
)