import asyncio

from core.bot import bot
from datetime import datetime

from db.models.models import Exchanges
from bot.keyboards.partner.result_exchange import *


# 30 минутное ожидание
async def update_keyboard_after_30_min(bot, chat_id, message_id, id_exchange):

    await asyncio.sleep(5)  # 30 минут

    # Проверка на завершённую сделку
    exchange_rate = await Exchanges.get(id=id_exchange)
    if exchange_rate.state == 'COMPLETED':
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
    await asyncio.sleep(23.5*60*60)  # 23,5 часа

    exchange_rate = await Exchanges.get(id=id_exchange)
    if exchange_rate.state != 'COMPLETED':
        await exchange_rate.update(
            state="COMPLETED"
        )

        return False, state_message_user
    
    return True, ''