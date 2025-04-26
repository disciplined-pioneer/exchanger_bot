from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="go_back")]
        ]
    )


