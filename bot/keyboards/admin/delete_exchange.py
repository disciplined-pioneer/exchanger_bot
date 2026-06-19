from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Exchanges

async def get_all_exchange_keyboard():

    all_exchange = await Exchanges.all()

    # Создаём клавиатуру с пустым inline_keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])  # Инициализируем пустой список

    for ex in all_exchange:
        button = InlineKeyboardButton(text=f'Обмен №{ex.id}', callback_data=f'ex_del:{ex.id}')
        keyboard.inline_keyboard.append([button])  # Добавляем кнопку в клавиатуру

    # Кнопка "Назад"
    button = InlineKeyboardButton(text=f'🔙 Назад', callback_data='go_back_menu')
    keyboard.inline_keyboard.append([button])

    return keyboard
