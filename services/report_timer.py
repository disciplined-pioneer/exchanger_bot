import os
import asyncio
import logging

from core.bot import bot
from settings import settings

from datetime import datetime, timedelta
from db.models.models import Exchanges
from db.models.mapped_columns import now_moscow


async def run_every_ten_minutes():
    
    logging.info("🚀 Активируем задачу.")
    await cancel_expired_exchanges()

    logging.info("🔁 Запущено ожидание 10 минут")
    await asyncio.sleep(600)
    

async def cancel_expired_exchanges():
    """
    Проверяет все обмены и отменяет те, что не обновлялись >= 15 минут и имеют статус NEW или же, если сделка не обновлялась больше одного дня
    Отправляет уведомления клиенту, партнёру и в группу.
    """
    logging.info("🔍 Проверка заявок на истечение времени...")

    all_exchanges = await Exchanges.all()
    now = now_moscow()

    for exchange in all_exchanges:
        if exchange.update_at is None:
            continue

        time_diff = now - exchange.update_at
        if (time_diff >= timedelta(minutes=15) and exchange.state == 'NEW') or (time_diff >= timedelta(days=1)):

            # Обновляем состояние обмена
            await exchange.update(
                state='CANCELLED'
            )

            logging.info(f"❌ Обмен ID {exchange.id} отменён (таймаут {time_diff}).")

            # Уведомляем участников и группу
            await bot.send_message(
                chat_id=exchange.partner_id,
                text=f'⏰ Заявка с пользователем {exchange.client_id} была отменена по таймауту'
            )

            await bot.send_message(
                chat_id=exchange.client_id,
                text=f'⏰ Заявка с партнёром {exchange.partner_id} была отменена по таймауту. Возможно, сейчас тех работы, повторите заявку в рабочее время или через 30 минут (в рабочее время)'
            )

            await bot.send_message(
                chat_id=settings.bot.GROUP_ID,
                text=f'⏰ Заявка {exchange.id} была отменена по таймауту'
            )

            
# Главный цикл репортера, запускается раз в 10 минут
async def reporter_loop():
    while True:
        try:
            await run_every_ten_minutes()

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
