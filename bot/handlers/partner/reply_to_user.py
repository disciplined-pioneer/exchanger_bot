from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot

from utils.user.exchange_confirmation import *
from bot.keyboards.partner.reply_to_user import *

from bot.templates.user.user_details import *
from bot.keyboards.user.user_details import *


router = Router()


# Обработчик кнопки "Ответить" пользователю
@router.callback_query(F.data == "reply_to_user")
async def reply_user(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    user_id = data.get('user_id', 0)
    await callback.message.edit_reply_markup(reply_markup=None)

    state_message = await callback.message.answer(
        text=f'Напишите сообщение клиенту: {user_id}',
        reply_markup=back_payment_confirmation
    )

    await state.set_state(MessagingStates.partner_message)
    await state.update_data(last_id_message=state_message.message_id)


# Отправляем сообщение пользователю
@router.message(MessagingStates.partner_message)
async def partner_message(message: types.Message, state: FSMContext):

    # Получаем данные
    data = await state.get_data()
    tg_id = message.from_user.id
    user_id = data.get('user_id', 0)
    last_id_message = data.get('last_id_message', 0)

    await state.set_state(None)

    try:
        
        # Убираем кнопки из старого сообщения, не меняя текст
        await bot.edit_message_reply_markup(
            chat_id=message.from_user.id,
            message_id=last_id_message,
            reply_markup=None
        )

        # Отправляем новое сообщение с подтверждением
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_sent_confirmation()
        )

        # Отправляем сообщение пользователю
        await bot.send_message(
            chat_id=user_id,
            text=await format_seller_message(tg_id, message.text),
            reply_markup=reply_to_partner
        )
    except:
        return


# Обработчик кнопки "Назад" в подтверждене оплаты
@router.callback_query(F.data == "back_payment_confirmation")
async def back_confirmation(callback: types.CallbackQuery, state: FSMContext):

    # Информация
    await callback.answer()
    await state.set_state(None)
    data = await state.get_data()
    partner_id = data.get('partner_id', '')
    details_user = data.get('details_user', '')
    message_type = data.get("message_type", '')

    # Убираем кнопки из старого сообщения
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # В зависимости от типа отправляем сообщение ПАРТНЁРУ
    if message_type in 'photo':

        # Отправляем сообщение партнёру
        await bot.send_photo(
            chat_id=partner_id,
            photo=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard()
        )

    elif message_type in 'document':

        # Отправляем сообщение партнёру
        await bot.send_document(
            chat_id=partner_id,
            document=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard()
        )

    else:

        # Партнёр
        await bot.send_message(
            chat_id=partner_id,
            text=format_user_details(details_user),
            reply_markup=create_payment_keyboard()
        )
