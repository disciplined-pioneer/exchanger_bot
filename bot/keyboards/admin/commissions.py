from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

request_partner_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📩 Запросить", callback_data="request")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="go_back_menu")]
    ]
)

def paid_commission_keyb(commissions):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"paid_commission:{commissions}")]
        ]
    )
    return keyb

back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Меню", callback_data="go_back_menu")]
    ]
)