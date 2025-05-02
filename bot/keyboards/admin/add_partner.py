from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="go_back_admin")]
    ]
)
