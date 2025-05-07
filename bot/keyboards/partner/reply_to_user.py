from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_payment_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_payment_confirmation")]
    ]
)

reply_to_partner = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data="not_receive_money")]
    ]
)