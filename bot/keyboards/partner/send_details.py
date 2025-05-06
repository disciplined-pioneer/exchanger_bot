from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def send_details(tg_id):
    return InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить реквизиты", callback_data=f"send_details_{tg_id}")]
    ]
)


confirm_details_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтверждаю", callback_data="confirm_details")],
        [InlineKeyboardButton(text="❌ Надо исправить", callback_data="edit_details")]
    ]
)

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data='payment_confirmed')]
    ]
)