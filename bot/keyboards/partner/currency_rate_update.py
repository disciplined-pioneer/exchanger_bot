from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="go_back")]
        ]
    )

send_details_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить реквизиты", callback_data="send_details")]
    ]
)
