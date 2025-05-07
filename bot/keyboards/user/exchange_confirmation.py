from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_confirmation")]
    ]
)

reply_to_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data="reply_to_user")]
    ]
)