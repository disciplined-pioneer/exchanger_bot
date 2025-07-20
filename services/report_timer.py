import os
import asyncio
import logging

from core.bot import bot
from settings import settings

from datetime import datetime, timedelta
from db.models.models import Exchanges
from db.models.mapped_columns import now_moscow


async def run_one_minutes():
    
    logging.info("🚀 Активируем задачу.")
    await cancel_expired_exchanges()

    logging.info("🔁 Запущено ожидание 1 минуты")
    await asyncio.sleep(60)
    

async def cancel_expired_exchanges():
    """
    Проверяет все обмены и отменяет те, что не обновлялись >= 15 минут и имеют статус NEW или же, если сделка не обновлялась больше одного дня
    Отправляет уведомления клиенту, партнёру и в группу.
    """
    logging.info("🔍 Проверка заявок на истечение времени...")

    all_exchanges = await Exchanges.exclude(state=['CANCELLED', 'COMPLETED', 'PAID', 'WAIT_PAYMENT']) # Все заявки, кроме уже отменённых или завершённых
    now = now_moscow()

    for exchange in all_exchanges:

        try:

            if exchange.update_at is None:
                continue

            time_diff = now - exchange.update_at
            if (time_diff >= timedelta(minutes=15) and exchange.state == 'NEW') or (time_diff >= timedelta(seconds=1)):

                # Обновляем состояние обмена
                await exchange.update(
                    state='CANCELLED'
                )

                try:
                    if exchange.last_id_msg is not None:
                        await bot.edit_message_reply_markup(
                            chat_id=exchange.client_id,
                            message_id=exchange.last_id_msg,
                            reply_markup=None
                        )
                except:
                    pass

                logging.info(f"❌ Обмен ID {exchange.id} отменён (таймаут {time_diff}).")

                try:
                    from db.models.models import Partners

                    partner = await Partners.get(tg_id=exchange.partner_id)
                    
                    # Уведомляем клиента
                    await bot.send_message(
                        chat_id=exchange.client_id,
                        text = (
                            f"❌ Заявка с партнёром {partner.name} была отменена по таймауту – ранее присланные реквизиты более не активны.\n\n"
                            f"НЕ СОВЕРШАЙТЕ НА НИХ ОПЛАТУ – ВЫ ПОТЕРЯЕТЕ ДЕНЬГИ.\n\n"
                            f"Если обмен для вас ещё актуален – создайте новую заявку."
                        )
                    )
                except Exception as e:
                    logging.warning(f"Не удалось отправить сообщение клиенту {exchange.client_id}: {e}")

                try:
                    # Уведомляем партнёра
                    await bot.send_message(
                        chat_id=exchange.partner_id,
                        text=f'⏰ Заявка с пользователем {exchange.partner_id} №{exchange.id} была отменена по таймауту'
                    )
                except Exception as e:
                    logging.warning(f"Не удалось отправить сообщение партнёру {exchange.partner_id}: {e}")

                try:
                    # Уведомляем группу
                    await bot.send_message(
                        chat_id=settings.bot.GROUP_ID,
                        text=f'⏰ Заявка №{exchange.id} была отменена по таймауту'
                    )
                except Exception as e:
                    logging.warning(f"Не удалось отправить сообщение в группу {settings.bot.GROUP_ID}: {e}")


        except Exception as e:
            logging.error(f"Произошла ошибка при отмене завки: {e}")
        
            
# Главный цикл репортера, запускается раз в 1 минуту
async def reporter_loop():
    while True:
        try:
            await run_one_minutes()

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
