from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_confirmation")]
    ]
)

def reply_to_user(ex_id):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ответить", callback_data=f"reply_to_user:{ex_id}")]
        ]
    )
    return keyb

new_message_partner_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написать новое сообщение", callback_data="not_receive_money")]
    ]
)