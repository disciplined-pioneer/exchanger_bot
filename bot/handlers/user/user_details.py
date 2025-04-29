import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from settings import settings
from utils.user.user_details import *

from bot.templates.user.user_details import *
from bot.keyboards.user.user_details import *

from db.models.models import ExchangeHistory, ExchangeRate


router = Router()


# Обработчик кнопки "Я оплатил"
@router.callback_query(F.data == "payment_confirmed")
async def payment_confirmed(callback: types.CallbackQuery, state: FSMContext):

    state_message = await callback.message.edit_text(photo_or_receipt_message)
    await state.set_state(PaymentState.waiting_for_receipt)  # Переходим в состояние ожидания файла
    await state.update_data({"last_id_message": state_message.message_id})


# Обработчик для получения фото или файла
@router.message(PaymentState.waiting_for_receipt)
async def handle_receipt(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    try:
        partner_number = int(data.get('partner_number', '')) - 1
        partner_id = settings.bot.PARTNERS[partner_number]

        if message.photo:
            sent_file = message.photo[-1]
            file_id = sent_file.file_id
            await state.update_data({"file_check": file_id})
            await bot.send_photo(partner_id, file_id, caption=payment_confirmation_message)

        elif message.document:
            file_id = message.document.file_id
            await state.update_data({"file_check": file_id})
            await bot.send_document(partner_id, file_id, caption=payment_confirmation_message)

        else:
            state_message = await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=photo_or_document_request_message
            )
            await state.update_data({"last_id_message": state_message.message_id})
            return

        # Сообщение пользователю
        exchange_type = data.get('exchange_type', '').split('_')[1].capitalize()
        state_message = await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text=generate_requisites_message(exchange_type)
                )
        await state.update_data({"last_id_message": state_message.message_id})
        await state.set_state(PaymentState.user_details)
        

    except:
        pass


# Обработчик для получения реквизитов пользователя
@router.message(PaymentState.user_details)
async def user_details(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    # Проверка на пустоту
    if not (message.photo or message.document or message.text):
        state_message = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text=photo_document_or_text_request_message,
            reply_markup=None
        )
        await state.update_data({"last_id_message": state_message.message_id})
        return

    # Логика по типу сообщения
    if message.photo:
        
        await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
        
        # Отправляем фотографию
        details = message.photo[-1].file_id
        sent_message = await bot.send_photo(
            chat_id=message.chat.id,
            photo=details,
            caption=format_confirm_details(),
            reply_markup=user_confirm_keyb
        )
        await state.update_data({"message_type": 'photo'})
        
    elif message.document:

        await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)

        # Отправляем документ
        details = message.document.file_id
        sent_message = await bot.send_document(
            chat_id=message.chat.id,
            document=details,
            caption=format_confirm_details(),
            reply_markup=user_confirm_keyb
        )
        await state.update_data({"message_type": 'document'})

    elif message.text:

        # Отправляем текст
        details = message.text
        sent_message = await bot.edit_message_text(
            chat_id=message.chat.id,
            text=format_confirm_details(details),
            message_id=last_bot_message_id,
            reply_markup=user_confirm_keyb
        )
        await state.update_data({"message_type": 'text'})


    # Сохраняем новое сообщение для трекинга
    await state.update_data({"last_id_message": sent_message.message_id,
                             'details_user': details})


# Обработчик кнопки "Подтверждаю"
@router.callback_query(F.data == "user_confirm_details")
async def user_confirm_details(callback: types.CallbackQuery, state: FSMContext):

    # Информация пользователя
    data = await state.get_data()
    id_exchange = data.get('id_exchange', '')
    partner_number = data.get('partner_number', '')
    partner_id = settings.bot.PARTNERS[int(partner_number)-1]
    details_user = data.get('details_user', '')
    currency = data.get('exchange_type', '').split('_')[0].upper()
    platform = data.get('exchange_type', '').split('_')[1].upper()
    sum_amount = data.get('sum_amout', '')
    cny_sum = round(sum_amount/await ExchangeRate.get_exchange_rate(f"{currency.lower()}_{platform.lower()}"))
    message_type = data.get("message_type", '')

    user_link = f'tg://user?id={callback.from_user.id}'

    # В зависимости от типа отправляем сообщение ПОЛЬЗОВАТЕЛЮ и ПАРТНЁРУ
    if message_type in 'photo':
        
        await callback.message.delete()

        # Отправляем сообщение пользователю
        state_message = await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=details_user,
            caption=generate_payment_message(cny_sum)
        )

        # Отправляем сообщение партнёру
        await bot.send_photo(
            chat_id=partner_id,
            photo=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard(user_link)
        )

    elif message_type in 'document':

        await callback.message.delete()

        # Отправляем сообщение пользователю
        state_message = await bot.send_document(
            chat_id=callback.message.chat.id,
            document=details_user,
            caption=generate_payment_message(cny_sum)
        )

        # Отправляем сообщение партнёру
        await bot.send_document(
            chat_id=partner_id,
            document=details_user,
            caption=format_user_details(),
            reply_markup=create_payment_keyboard(user_link)
        )

    else:

        state_message = await callback.message.edit_text(generate_payment_message(cny_sum, details_user)) # Пользователь

        # Партнёр
        await bot.send_message(
            chat_id=partner_id,
            text=format_user_details(details_user),
            reply_markup=create_payment_keyboard(user_link)
        )
    
    await state.update_data({"last_id_message": state_message.message_id})

    # Изменяем статус
    exchange_rate = await ExchangeHistory.get(id=id_exchange)
    await exchange_rate.update(
        status="waiting_for_payment_confirmation"
    )

    # Ждём 5 минут и проверяем статус
    await asyncio.sleep(300)
    exchange = await ExchangeHistory.get(id=id_exchange)
    status = exchange.status
    if status == 'waiting_for_payment_confirmation':
        state_message = await callback.message.answer(
            text=get_no_payment_instructions(),
            reply_markup=support_keyb,
            parse_mode="MarkdownV2"
        )

        await state.update_data({"last_id_message": state_message.message_id})


# Обработчик кнопки "Надо исправить"
@router.callback_query(F.data == "user_edit_details")
async def user_edit_details(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    exchange_type = data.get('exchange_type', '').split('_')[1].capitalize()
    message_type = data.get("message_type")
    
    # В зависимости от типа отправляем сообщение
    if message_type in ['photo', 'document']:
        await callback.message.delete()
        state_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=generate_requisites_message(exchange_type)
        )
    else:
        state_message = await callback.message.edit_text(
            text=generate_requisites_message(exchange_type)
        )

    await state.set_state(PaymentState.user_details)
    await state.update_data({"last_id_message": state_message.message_id})