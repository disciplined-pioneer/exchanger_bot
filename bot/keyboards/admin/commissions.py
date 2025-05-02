from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

request_partner_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📩 Запросить", callback_data="request")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="go_back_menu")]
    ]
)

paid_commission_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid_commission")]
    ]
)

