import asyncio

from core.bot import bot
from db.models.models import ExchangeHistory
from bot.keyboards.partner.result_exchange import *


async def update_keyboard_after_30_min(bot, chat_id, message_id, id_exchange):

    await asyncio.sleep(30 * 60)  # 30 минут

    # Проверка на завершённую сделку
    exchange_rate = await ExchangeHistory.get(id=id_exchange)
    if exchange_rate.status == 'exchange_completed':
        return True, '' # Не нужно изменять

    # Изменяем кнопку
    try:
        state_message_user = await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=get_full_exchange_completion_keyboard()
        )
    except Exception as e:
        print(f"Ошибка при обновлении клавиатуры: {e}")

    # Проверка на то, что сделка завершена
    await asyncio.sleep(23.5 * 60 * 60)  # 23,5 часа

    exchange_rate = await ExchangeHistory.get(id=id_exchange)
    if exchange_rate.status != 'exchange_completed':
        await exchange_rate.update(
            status="exchange_completed"
        )

        return False, state_message_user
    
    return True, ''