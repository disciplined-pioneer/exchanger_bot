from settings import settings
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Генерация кнопок "Партнёры"
def generate_partner_buttons() -> InlineKeyboardMarkup:

    # Устанавливаем row_width=1 и передаем inline_keyboard
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Партнёр {idx}", callback_data=f"partner_{idx}")]
            for idx in range(1, len(settings.bot.PARTNERS) + 1)
        ],
        row_width=1
    )
    
    return keyboard

