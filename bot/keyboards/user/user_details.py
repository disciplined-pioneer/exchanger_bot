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

keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="")],
        [InlineKeyboardButton(text="❌ Деньги не пришли", callback_data="")],
        [InlineKeyboardButton(text=" Сложности с оплатой, написать клиенту в чат", url=settings.bot.SUPPORT_LINK)]
    ]
)


def create_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я оплатил", callback_data="user_paid")],
            [InlineKeyboardButton(text="❌ Деньги не пришли", callback_data="user_not_paid")],
            [InlineKeyboardButton(text="💬 Сложности с оплатой, написать клиенту в чат",url=settings.bot.SUPPORT_LINK)]
        ]
    )
