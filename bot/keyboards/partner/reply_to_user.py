from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_payment_confirmation(ex_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_payment_confirmation:{ex_id}")]
        ]
    )

reply_to_partner = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data="not_receive_money")]
    ]
)

def reply_to_user(ex_id):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Написать новое сообщение", callback_data=f"reply_to_user:{ex_id}")]
        ]
    )
    return keyb