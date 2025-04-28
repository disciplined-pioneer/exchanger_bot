from settings import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

user_confirm_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтверждаю", callback_data="user_confirm_details")],
        [InlineKeyboardButton(text="❌ Надо исправить", callback_data="user_edit_details")]
    ]
)

support_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поддержка", url=settings.bot.SUPPORT_LINK)]
    ]
)