from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="go_back")]
        ]
    )


back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Меню", callback_data="go_back_menu")]
    ]
)