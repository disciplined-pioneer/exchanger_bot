import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.user_details import *

from bot.templates.user.user_details import *
from bot.keyboards.user.user_details import *
from bot.keyboards.partner.result_exchange import get_full_exchange_completion_keyboard

from db.models.models import Exchanges, now_moscow


router = Router()


# Обработчик кнопки "Я оплатил"
@router.callback_query(F.data == "payment_confirmed")
async def payment_confirmed(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    id_exchange = data.get('id_exchange', 0)

    # Изменяем статус
    exchange_rate = await Exchanges.get(id=id_exchange)
    await exchange_rate.update(
        state="WAIT_PAYMENT",
        update_at=now_moscow()
    )

    try:
        # Убираем кнопки из старого сообщения, не меняя текст
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    state_message = await callback.message.answer(photo_or_receipt_message)
    await state.update_data({"last_id_message": state_message.message_id})
    await state.set_state(PaymentState.waiting_for_receipt)  # Переходим в состояние ожидания файла


# Обработчик для получения фото или файла
@router.message(PaymentState.waiting_for_receipt)
async def handle_receipt(message: types.Message, state: FSMContext):

    # Данные
    await message.delete()
    data = await state.get_data()
    tg_id = message.from_user.id
    partner_id = data.get("partner_id", '')
    id_exchange = data.get('id_exchange', 0)

    try:

        if message.photo:
            sent_file = message.photo[-1]
            file_id = sent_file.file_id
            await state.update_data({"file_check": file_id})
            exchange_rate = await Exchanges.get(id=id_exchange)
            await bot.send_photo(exchange_rate.partner.tg_id, file_id, caption=payment_confirmation_message(tg_id))

        elif message.document:
            file_id = message.document.file_id
            await state.update_data({"file_check": file_id})
            exchange_rate = await Exchanges.get(id=id_exchange)
            await bot.send_document(exchange_rate.partner.tg_id, file_id, caption=payment_confirmation_message(tg_id))

        else:
            state_message = await bot.send_message(
                chat_id=message.chat.id,
                text=photo_or_document_request_message
            )
            await state.update_data({"last_id_message": state_message.message_id})
            return
        
        # Изменяем поле с чеком
        exchange_rate = await Exchanges.get(id=id_exchange)
        await exchange_rate.update(
            payment_check=file_id,
            update_at=now_moscow()
        )

        # Сообщение пользователю
        platform = data.get('platform', '')
        state_message = await bot.send_message(
            chat_id=message.chat.id,
            text=generate_requisites_message(platform)
        )
        await state.update_data({"last_id_message": state_message.message_id})
        await state.set_state(PaymentState.user_details)

        # Логгирование в группу
        await bot.send_message(
            chat_id=settings.bot.GROUP_ID,
            text=format_receipt_log(tg_id, id_exchange)
        )

    except:
        pass


# Обработчик для получения реквизитов пользователя
@router.message(PaymentState.user_details)
async def user_details(message: types.Message, state: FSMContext):

    try:
        await message.delete()
        data = await state.get_data()
        last_bot_message_id = data.get("last_id_message")

        # Проверка на пустоту
        if not (message.photo or message.document or message.text):
            await bot.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                reply_markup=None
            )
            state_message = await bot.send_message(
                chat_id=message.chat.id,
                text=photo_document_or_text_request_message
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

            await bot.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                reply_markup=None
            )
            sent_message = await bot.send_message(
                chat_id=message.chat.id,
                text=format_confirm_details(details),
                reply_markup=user_confirm_keyb
            )
            await state.update_data({"message_type": 'text'})

        # Сохраняем новое сообщение для трекинга
        await state.update_data({"last_id_message": sent_message.message_id,
                                'details_user': details})
        
        await state.set_state(None)  # Снимаем состояние

    except:
        pass


# Обработчик кнопки "Подтверждаю"
@router.callback_query(F.data == "user_confirm_details")
async def user_confirm_details(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    tg_id = callback.from_user.id
    id_exchange = data.get('id_exchange', '')
    partner_id = data.get('partner_id', '')
    details_user = data.get('details_user', '')
    cny_sum = data.get('cny_sum', '')
    message_type = data.get("message_type", '')

    # Сохраняем для использования партнёром
    exchange = await Exchanges.get(id=id_exchange)
    data = exchange.data
    data['details_user'] = details_user
    data['message_type'] = message_type

    await exchange.update(data=data)

    if message_type == 'photo':

        await callback.message.delete()

        # Сообщение пользователю
        state_message = await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=details_user,
            caption=generate_payment_message(cny_sum)
        )

        # Сообщение партнёру
        exchange = await Exchanges.get(id=id_exchange)
        await bot.send_photo(
            chat_id=exchange.partner.tg_id,
            photo=details_user,
            caption=format_user_details(tg_id=tg_id),
            reply_markup=create_payment_keyboard(id_exchange)
        )

    elif message_type == 'document':

        await callback.message.delete()

        # Сообщение пользователю
        state_message = await bot.send_document(
            chat_id=callback.message.chat.id,
            document=details_user,
            caption=generate_payment_message(cny_sum)
        )

        # Сообщение партнёру
        exchange = await Exchanges.get(id=id_exchange)
        await bot.send_document(
            chat_id=exchange.partner.tg_id,
            document=details_user,
            caption=format_user_details(tg_id=tg_id),
            reply_markup=create_payment_keyboard(id_exchange)
        )

    else:

        state_message = await callback.message.edit_text(
            generate_payment_message(cny_sum, f"\nРеквизиты:\n{details_user}")
        )

        exchange = await Exchanges.get(id=id_exchange)
        await bot.send_message(
            chat_id=exchange.partner.tg_id,
            text=format_user_details(details=details_user, tg_id=tg_id),
            reply_markup=create_payment_keyboard()
        )

    await state.set_state(None)
    await state.update_data({"last_id_message": state_message.message_id})

    # Ждём 15 минут и проверяем статус
    await asyncio.sleep(15*60)
    exchange = await Exchanges.get(id=id_exchange)
    state_exchange = exchange.state
    if state_exchange == 'WAIT_PAYMENT':
        await callback.message.answer(
            text=get_no_payment_instructions(),
            reply_markup=support_keyb
        )


# Обработка кнопки "Назад" после 15 минут
@router.callback_query(F.data == "back_end_deal")
async def back_end_deal(callback: types.CallbackQuery, state: FSMContext):

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    state_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=complete_deal_instruction_msg,
        reply_markup=get_full_exchange_completion_keyboard()
    )
    await state.update_data({"last_id_message": state_message.message_id})


# Обработчик кнопки "Надо исправить"
@router.callback_query(F.data == "user_edit_details")
async def user_edit_details(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    platform = data.get('platform', '')
    message_type = data.get("message_type")
    
    # В зависимости от типа отправляем сообщение
    if message_type in ['photo', 'document']:
        await callback.message.delete()
        state_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=generate_requisites_message(platform)
        )
    else:
        try:
            # Убираем кнопки из старого сообщения, не меняя текст
            await callback.message.edit_reply_markup(reply_markup=None)
        except:
            pass
        state_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=generate_requisites_message(platform)
        )

    await state.set_state(PaymentState.user_details)
    await state.update_data({"last_id_message": state_message.message_id})
