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
async def reply_to_user(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user_id = data.get('user_id', 0)
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        text=f'Напишите сообщение клиенту: {user_id}',
        reply_markup=back_payment_confirmation
    )

    #await state.set_state(MessagingStates.partner_message)


# Обработчик кнопки "Назад" в подтверждене оплаты
@router.callback_query(F.data == "back_payment_confirmation")
async def backpaymentconfirmation(callback: types.CallbackQuery, state: FSMContext):

    # Информация
    data = await state.get_data()
    partner_id = data.get('partner_id', '')
    details_user = data.get('details_user', '')
    message_type = data.get("message_type", '')

    user_link = f'tg://user?id={callback.from_user.id}'

    # В зависимости от типа отправляем сообщение ПОЛЬЗОВАТЕЛЮ и ПАРТНЁРУ
    if message_type in 'photo':
        
        await callback.message.delete()

        # Отправляем сообщение партнёру
        await bot.send_photo(
            chat_id=partner_id,
            photo=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard(user_link)
        )

    elif message_type in 'document':

        await callback.message.delete()

        # Отправляем сообщение партнёру
        await bot.send_document(
            chat_id=partner_id,
            document=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard(user_link)
        )

    else:

        # Партнёр
        await bot.send_message(
            chat_id=partner_id,
            text=format_user_details(details_user),
            reply_markup=create_payment_keyboard(user_link)
        )
