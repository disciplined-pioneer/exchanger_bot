from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from core.bot import bot

from utils.user.exchange_confirmation import *
from bot.keyboards.partner.reply_to_user import *

from bot.templates.user.user_details import *
from bot.keyboards.user.user_details import *

from db.models.models import Exchanges


router = Router()


# Обработчик кнопки "Ответить" пользователю
@router.callback_query(F.data.startswith("reply_to_user"))
async def reply_user(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    id_exchange = int(callback.data.split(':')[1])
    exchange_rate = await Exchanges.get(id=id_exchange)
    user_id = exchange_rate.client.tg_id
    await callback.message.edit_reply_markup(reply_markup=None)

    state_message = await callback.message.answer(
        text=generate_client_message_text(user_id),
        reply_markup=back_payment_confirmation(exchange_rate.id)
    )

    await state.set_state(MessagingStates.partner_message)
    await state.update_data(last_id_message=state_message.message_id, ex_id=exchange_rate.id)


# Отправляем сообщение пользователю
@router.message(StateFilter(MessagingStates.partner_message), F.text)
async def partner_message(message: types.Message, state: FSMContext):

    # Получаем данные
    data = await state.get_data()
    tg_id = message.from_user.id
    ex_id = data.get('ex_id')
    last_id_message = data.get('last_id_message')

    exchange_rate = await Exchanges.get(id=int(ex_id))
    user_id = exchange_rate.client.tg_id
    await state.update_data(ex_id=None)

    try:

        # Отправляем сообщение пользователю
        await bot.send_message(
            chat_id=user_id,
            text=await format_seller_message(tg_id, message.text),
            reply_markup=reply_to_partner
        )
        
        # Убираем кнопки из старого сообщения, не меняя текст
        await bot.edit_message_reply_markup(
            chat_id=message.from_user.id,
            message_id=last_id_message,
            reply_markup=None
        )

        # Отправляем новое сообщение с подтверждением
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_sent_confirmation(),
            reply_markup=reply_to_user(ex_id)
        )

    except Exception as e:
        print(e)
        return
    print(data)
    await state.set_state(None)


# Обработчик кнопки "Назад" в подтверждене оплаты
@router.callback_query(F.data.startswith("back_payment_confirmation"))
async def back_confirmation(callback: types.CallbackQuery, state: FSMContext):

    # Информация
    await callback.answer()

    id_exchange = int(callback.data.split(':')[1])
    exchange = await Exchanges.get(id=int(id_exchange))
    data = exchange.data

    partner_id = data.get('partner_id', '')
    details_user = data.get('details_user', '')
    message_type = data.get("message_type", '')

    await state.update_data(ex_id=None)

    # Убираем кнопки из старого сообщения
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass


    # В зависимости от типа отправляем сообщение ПАРТНЁРУ
    if message_type in 'photo':

        # Отправляем сообщение партнёру
        await bot.send_photo(
            chat_id=exchange.partner.tg_id,
            photo=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard(id_exchange)
        )

    elif message_type in 'document':

        # Отправляем сообщение партнёру
        await bot.send_document(
            chat_id=exchange.partner.tg_id,
            document=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard(id_exchange)
        )

    else:

        # Партнёр
        await bot.send_message(
            chat_id=exchange.partner.tg_id,
            text=format_user_details(details_user),
            reply_markup=create_payment_keyboard(id_exchange)
        )

    await state.set_state(None)