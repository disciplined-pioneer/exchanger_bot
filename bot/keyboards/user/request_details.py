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
                text=f"Партнёр {idx} | CNY ~ {min(result.usdt_alipay, result.usdt_alipay)}$ ~ {min(result.rub_alipay, result.rub_wechat)}Р", 
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


exchange_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💱 Совершить обмен", callback_data="make_exchange")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_partner")]
    ]
)

exchange_methods_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="RUB → Alipay", callback_data="exchange_rub_alipay")],
        [InlineKeyboardButton(text="RUB → WeChat", callback_data="exchange_rub_wechat")],
        [InlineKeyboardButton(text="USDT → Alipay", callback_data="exchange_usdt_alipay")],
        [InlineKeyboardButton(text="USDT → WeChat", callback_data="exchange_usdt_wechat")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_partner")]
    ]
)

confirm_exchange_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Верно, начать обмен", callback_data="start_exchange")],
        [InlineKeyboardButton(text="❌ Отменить обмен", callback_data="back_partner")]
    ]
)
