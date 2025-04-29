from settings import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_partial_exchange_completion_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я получил CNY, завершить обмен", callback_data="confirm_cny_received")]
        ]
    )


def get_full_exchange_completion_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я получил CNY, завершить обмен", callback_data="confirm_cny_received")],
            [InlineKeyboardButton(text="❌ Я не получил, написать в поддержку", url=settings.bot.SUPPORT_LINK)]
        ]
    )
