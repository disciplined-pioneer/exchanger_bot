from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from core.bot import bot
from utils.user.user_details import *
from utils.partner.result_exchange import *

from bot.templates.partner.result_exchange import *

from settings import settings
from db.models.models import Exchanges, now_moscow


router = Router()
    

# Обработчик кнопки "Я оплатил" у партнёра
@router.callback_query(F.data == "paid_partner")
async def user_paid(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    tg_id = callback.from_user.id
    user_id = data.get('user_id', 0)
    id_exchange = data.get('id_exchange', 0)

    # Изменяем статус
    exchange_rate = await Exchanges.get(id=id_exchange)
    await exchange_rate.update(
        state="PAID",
        update_at=now_moscow()
    )

    # Убираем кнопки из старого сообщения, не меняя текст
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # Отправляем сообщение пользователю только с первой кнопкой
    sent_message_user = await bot.send_message(
        chat_id=user_id,
        text=partner_payment_confirmed_message,
        reply_markup=get_partial_exchange_completion_keyboard()
    )

    # Отправляем новое сообщение с подтверждением оплаты
    await callback.message.answer(payment_confirmed_message)
    
    # Логгирование в группу
    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text=f"✅ Партнёр {tg_id} подтвердил оплату по заявке {id_exchange}" 
    )

    # Отложенное обновление клавиатуры через 30 минут
    result, state_message_user_new = await update_keyboard_after_30_min(bot, user_id, sent_message_user.message_id, id_exchange)
    if not result:
        await bot.delete_message(chat_id=user_id, message_id=state_message_user_new.message_id)
        await bot.send_message(
            chat_id=user_id,
            text=deal_auto_completed_message
        )

    await state.clear()

    
# Обработчик кнопки "Деньги не пришли" у партнёра
@router.callback_query(F.data == "not_paid_partner")
async def user_not_paid(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    user_id = data.get('user_id', '')

    # Убираем кнопки из старого сообщения, не меняя текст
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # Отправляем новое сообщение с подтверждением партнёру
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
