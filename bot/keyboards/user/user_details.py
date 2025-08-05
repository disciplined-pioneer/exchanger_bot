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
        [InlineKeyboardButton(text="Поддержка", url=settings.bot.SUPPORT_LINK)],
        [InlineKeyboardButton(text="Написать партнёру", callback_data="not_receive_money")],
        [InlineKeyboardButton(text="Назад", callback_data="back_end_deal")]
    ]
)

def create_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid_partner")],
            [InlineKeyboardButton(text="❌ Деньги не пришли", callback_data="not_paid_partner")],
            [InlineKeyboardButton(text="💬 Сложности с оплатой, написать клиенту в чат", callback_data='reply_to_user')]
        ]
    )
