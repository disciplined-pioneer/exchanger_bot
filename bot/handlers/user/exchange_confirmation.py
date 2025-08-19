from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from core.bot import bot
from settings import settings
from utils.user.user_details import *
from utils.user.exchange_confirmation import *

from bot.keyboards.user.exchange_confirmation import *
from bot.templates.user.exchange_confirmation import *

from bot.templates.partner.result_exchange import *
from bot.keyboards.partner.result_exchange import *

from db.models.models import Exchanges, now_moscow


router = Router()


# Обработчик кнопки "Я получил деньги"
@router.callback_query(F.data == "confirm_receipt_money")
async def confirm_receipt_money(callback: types.CallbackQuery, state: FSMContext):
    
    await callback.answer()
    data = await state.get_data()
    id_exchange = data.get('id_exchange', 0)
    partner_id = data.get('partner_id', 0)

    # Изменяем статус
    exchange_rate = await Exchanges.get(id=id_exchange)
    await exchange_rate.update(
        state="COMPLETED",
        update_at=now_moscow()
    )
    
    try:
        # Убираем кнопки из старого сообщения, не меняя текст
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass
    await callback.message.answer(exchange_completed_message)

    # Сообщение партнёру
    await bot.send_message(
        chat_id=partner_id,
        text=exchange_completed_message_partner(callback.from_user.id, id_exchange)
    )

    # Уведомляем группу
    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text=exchange_completed_message_partner(callback.from_user.id, id_exchange)
    )

    # Удаляем id сделки из списка
    partner_state = FSMContext(
        storage=state.storage,
        key=StorageKey(bot_id=state.key.bot_id, chat_id=partner_id, user_id=partner_id)
    )
    partner_data = await partner_state.get_data()
    ex_ids = partner_data.get('ex_ids', {})
    ex_ids.pop(exchange_rate.id, None)
    await partner_state.update_data(ex_ids=ex_ids)

    await state.clear()


# Обработчик кнопки "Я не получил деньги"
@router.callback_query(F.data == "not_receive_money")
async def not_receive_money(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    try:
        # Убираем кнопки из старого сообщения, не меняя текст
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    state_message = await callback.message.answer(
        text=prompt_message_to_seller(),
        reply_markup=back_confirmation
    )
    await state.set_state(MessagingStates.user_message)
    await state.update_data(last_id_message=state_message.message_id)


# Отправляем сообщение партнёру
@router.message(StateFilter(MessagingStates.user_message), F.text)
async def user_message(message: types.Message, state: FSMContext):

    # Получаем данные
    data = await state.get_data()
    tg_id = message.from_user.id
    partner_id = data.get('partner_id', 0)
    id_exchange = data.get('id_exchange', 0)
    last_id_message = data.get('last_id_message', 0)

    await state.set_state(None)

    try:

        # Отправляем сообщение партнёру
        await bot.send_message(
            chat_id=partner_id,
            text=format_message_to_partner(tg_id, message.text),
            reply_markup=reply_to_user(id_exchange)
        )

        # Убираем клавиатуру с предыдущего сообщения, не меняя текст
        await bot.edit_message_reply_markup(
            chat_id=message.from_user.id,
            message_id=last_id_message,
            reply_markup=None
        )

        # Отправляем новое сообщение вместо редактирования
        await bot.send_message(
            chat_id=message.from_user.id,
            text=confirmation_message(),
            reply_markup=new_message_partner_keyb
        )
        
    except:
        pass


# Обработка кнопки "Назад" в подтверждение оплаты
@router.callback_query(F.data == "back_confirmation")
async def backconfirmation(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.set_state(None) # Если вернулись от "Назад"
    await callback.message.edit_text(
        text=partner_payment_confirmed_message,
        reply_markup=get_full_exchange_completion_keyboard()
    )
