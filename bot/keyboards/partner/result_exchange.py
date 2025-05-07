from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_partial_exchange_completion_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я получил CNY, завершить обмен", callback_data="confirm_receipt_money")]
        ]
    )


def get_full_exchange_completion_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я получил CNY, завершить обмен", callback_data="confirm_receipt_money")],
            [InlineKeyboardButton(text="❌ Я не получил, написать партнёру", callback_data="not_receive_money")]
        ]
    )