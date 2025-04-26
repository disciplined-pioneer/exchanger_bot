from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

send_details_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить реквизиты", callback_data="send_details")]
    ]
)


confirm_details_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтверждаю", callback_data="confirm_details")],
        [InlineKeyboardButton(text="❌ Надо исправить", callback_data="edit_details")]
    ]
)