from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.user_details import *
from utils.user.exchange_confirmation import *

from bot.keyboards.user.exchange_confirmation import *
from bot.templates.user.exchange_confirmation import *

from bot.templates.partner.result_exchange import *
from bot.keyboards.partner.result_exchange import *

from datetime import datetime
from db.models.models import Exchanges


router = Router()


# Обработчик кнопки "Я получил деньги"
@router.callback_query(F.data == "confirm_receipt_money")
async def confirm_receipt_money(callback: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    id_exchange = data.get('id_exchange', 0)
    partner_id = data.get('partner_id', 0)

    # Изменяем статус
    exchange_rate = await Exchanges.get(id=id_exchange)
    await exchange_rate.update(
        state="COMPLETED",
        update_at=datetime.now()
    )

    await callback.message.edit_text(exchange_completed_message)

    # Сообщение партнёру
    await bot.send_message(
        chat_id=partner_id,
        text=exchange_completed_message_partner(callback.from_user.id, id_exchange)
    )

    
    await state.clear()


# Обработчик кнопки "Я не получил деньги"
@router.callback_query(F.data == "not_receive_money")
async def not_receive_money(callback: types.CallbackQuery, state: FSMContext):

    state_message = await callback.message.edit_text(
        text='Напишите сообщение продавцу',
        reply_markup=back_confirmation
    )
    await state.set_state(MessagingStates.user_message)
    await state.update_data(last_id_message=state_message.message_id)


# Отправляем сообщение партнёру
@router.message(MessagingStates.user_message)
async def user_message(message: types.Message, state: FSMContext):

    # Получаем данные
    data = await state.get_data()
    tg_id  = message.from_user.id
    partner_id = data.get('partner_id', 0)
    last_id_message = data.get('last_id_message', 0)

    await state.set_state(None)

    try:
        # Удаляем сообщения
        await bot.edit_message_text(
            text='Сообщение было отправлено партнёру',
            chat_id=message.from_user.id,
            message_id=last_id_message
        )

        # Отправляем сообщение партнёру
        await bot.send_message(
            chat_id=partner_id,
            text=f'Сообщение от клиента {tg_id}: {message.text}',
            reply_markup=reply_to_user
        )
    except Exception as e:
        print(e)


# Обработка кнопки "Назад" в подтверждение оплаты
@router.callback_query(F.data == "back_confirmation")
async def backconfirmation(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(None) # Если вернулись от "Назад"
    await callback.message.edit_text(
        text=partner_payment_confirmed_message,
        reply_markup=get_full_exchange_completion_keyboard()
    )