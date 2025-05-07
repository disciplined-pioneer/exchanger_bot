from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_payment_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_payment_confirmation")]
    ]
)