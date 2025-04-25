from settings import settings
from db.models.models import ExchangeRate

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Генерация кнопок "Партнёры"
async def generate_partner_buttons() -> InlineKeyboardMarkup:

    # Устанавливаем row_width=1 и передаем inline_keyboard
    result = await ExchangeRate.get(id=1)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            # Генерация кнопок партнёров
            [InlineKeyboardButton(
                text=f"Партнёр {idx} | CNY ~ {min(result.usd_alipay, result.usd_alipay)}$ ~ {min(result.rub_alipay, result.rub_wechat)}Р", 
                callback_data=f"partner_{idx}"
            )]
            for idx in range(1, len(settings.bot.PARTNERS) + 1)
        ] +
        # Добавляем кнопку "Назад"
        [
            [InlineKeyboardButton(
                text="🔙 Назад", 
                callback_data="back_menu"
            )]
        ],
        row_width=1
    )

    return keyboard


