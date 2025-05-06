from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from core.bot import bot
from utils.user.user_details import *
from utils.partner.send_details import *

from bot.templates.partner.result_exchange import *
from bot.keyboards.partner.result_exchange import *

from datetime import datetime
from db.models.models import Exchanges


router = Router()
    

# Обработчик кнопки "Я оплатил" у партнёра
@router.callback_query(F.data == "paid_partner")
async def user_paid(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user_id = data.get('user_id', 0)
    id_exchange = data.get('id_exchange', 0)

    # Изменяем статус
    exchange_rate = await Exchanges.get(id=id_exchange)
    await exchange_rate.update(
        state="PAID",
        update_at=datetime.now()
    )

    await callback.message.delete()
    await callback.message.answer(payment_confirmed_message)

    # Отправляем сообщение пользователю только с первой кнопкой
    sent_message_user = await bot.send_message(
        chat_id=user_id,
        text=partner_payment_confirmed_message,
        reply_markup=get_partial_exchange_completion_keyboard()
    )

    # Отложенное обновление клавиатуры через 30 минут
    result, state_message_user_new = await update_keyboard_after_30_min(bot, user_id, sent_message_user.message_id, id_exchange)
    if not result:
        await bot.delete_message(chat_id=user_id, message_id=state_message_user_new.message_id)
        await bot.send_message(
            chat_id=user_id,
            text=deal_auto_completed_message
        )

    
# Обработчик кнопки "Деньги не пришли" у партнёра
@router.callback_query(F.data == "not_paid_partner")
async def user_not_paid(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user_id = data.get('user_id', '')
    
    # Сообщение партнёру
    await callback.message.delete()
    await callback.message.answer(message_sent_to_user)

    # Отправляем сообщение пользователю
    state_message = await bot.send_message(
        chat_id=user_id,
        text=payment_not_received_message
    )

    # Устанавливаем состояние для пользователя по его id
    user_state = FSMContext(
        storage=state.storage,
        key=StorageKey(bot_id=state.key.bot_id, chat_id=user_id, user_id=user_id)
    )

    await user_state.set_state(PaymentState.waiting_for_receipt)  # Переходим в состояние ожидания файла
    await user_state.update_data({"last_id_message": state_message.message_id})
