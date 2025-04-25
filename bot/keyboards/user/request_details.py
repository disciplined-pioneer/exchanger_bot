from settings import settings
from db.models.models import ExchangeRate
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Генерация кнопок "Партнёры"
async def generate_partner_buttons() -> InlineKeyboardMarkup:

    try:
        # Пытаемся получить данные из базы
        result = await ExchangeRate.get(id=1)
        
        # Проверяем, что результат не None
        if result is None:
            # Если результат None, генерируем клавиатуру с сообщением об ошибке
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Ошибка", callback_data="error")]
                ],
                row_width=1
            )
            return keyboard
        
        # Если результат есть, генерируем клавиатуру с партнерами
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"Партнёр {idx} | CNY ~ {min(result.usd_alipay, result.usd_alipay)}$ ~ {min(result.rub_alipay, result.rub_wechat)}Р", 
                    callback_data=f"partner_{idx}"
                )]
                for idx in range(1, len(settings.bot.PARTNERS) + 1)
            ],
            row_width=1
        )
        
        return keyboard

    except Exception as e:
        # Логируем ошибку и возвращаем клавиатуру с сообщением об ошибке
        print(f"Ошибка при получении данных: {e}")
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Ошибка", callback_data="error")]
            ],
            row_width=1
        )
        return keyboard
