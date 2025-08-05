from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_confirmation")]
    ]
)

reply_to_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data="reply_to_user")]
    ]
)

new_message_partner_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написать новое сообщение", callback_data="not_receive_money")]
    ]
)