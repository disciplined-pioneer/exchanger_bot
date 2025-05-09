import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.user_details import *

from bot.templates.user.user_details import *
from bot.keyboards.user.user_details import *

from datetime import datetime
from db.models.models import Exchanges


router = Router()


# Обработчик кнопки "Я оплатил"
@router.callback_query(F.data == "payment_confirmed")
async def payment_confirmed(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    id_exchange = data.get('id_exchange', 0)

    # Изменяем статус
    exchange_rate = await Exchanges.get(id=id_exchange)
    await exchange_rate.update(
        state="WAIT_PAYMENT",
        update_at=datetime.now()
    )

    state_message = await callback.message.edit_text(photo_or_receipt_message)
    await state.update_data({"last_id_message": state_message.message_id})
    await state.set_state(PaymentState.waiting_for_receipt)  # Переходим в состояние ожидания файла


# Обработчик для получения фото или файла
@router.message(PaymentState.waiting_for_receipt)
async def handle_receipt(message: types.Message, state: FSMContext):

    data = await state.get_data()
    id_exchange = data.get('id_exchange', 0)

    await message.delete()
    data = await state.get_data()
    tg_id = message.from_user.id
    partner_id = data.get("partner_id", '')
    last_bot_message_id = data.get("last_id_message", 0)

    try:

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
        
        # Изменяем поле с чеком
        exchange_rate = await Exchanges.get(id=id_exchange)
        await exchange_rate.update(
            payment_check=file_id,
            update_at=datetime.now()
        )

        # Сообщение пользователю
        platform = data.get('platform', '')
        state_message = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text=generate_requisites_message(platform)
        )
        await state.update_data({"last_id_message": state_message.message_id})
        await state.set_state(PaymentState.user_details)

        # Логгирование в группу
        await bot.send_message(
            chat_id=settings.bot.GROUP_ID,
            text=f"📎 Клиент {tg_id} отправил чек по заявке {id_exchange}"
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
        
        await state.set_state(None)  # Снимаем состояние

    except:
        pass


# Обработчик кнопки "Подтверждаю"
@router.callback_query(F.data == "user_confirm_details")
async def user_confirm_details(callback: types.CallbackQuery, state: FSMContext):

    # Информация пользователя
    data = await state.get_data()
    id_exchange = data.get('id_exchange', '')
    partner_id = data.get('partner_id', '')
    details_user = data.get('details_user', '')
    cny_sum = data.get('cny_sum', '')
    message_type = data.get("message_type", '')

    from aiogram.fsm.storage.base import StorageKey
    partner_state = FSMContext(
        storage=state.storage,
        key=StorageKey(bot_id=state.key.bot_id, chat_id=partner_id, user_id=partner_id)
    )
    await partner_state.update_data(details_user=details_user, message_type=message_type)


    #user_link = f'tg://user?id={callback.from_user.id}'

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
            reply_markup=create_payment_keyboard()
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
            reply_markup=create_payment_keyboard()
        )

    else:

        state_message = await callback.message.edit_text(generate_payment_message(cny_sum, f"\nРеквизиты:\n{details_user}")) # Пользователь

        # Партнёр
        await bot.send_message(
            chat_id=partner_id,
            text=format_user_details(details_user),
            reply_markup=create_payment_keyboard()
        )
    
    await state.set_state(None)
    await state.update_data({"last_id_message": state_message.message_id})

    # Ждём 5 минут и проверяем статус
    await asyncio.sleep(5*60)
    exchange = await Exchanges.get(id=id_exchange)
    state = exchange.state
    if state == 'WAIT_PAYMENT':
        state_message = await callback.message.answer(
            text=get_no_payment_instructions(partner_id),
            reply_markup=support_keyb,
            parse_mode="MarkdownV2"
        )


# Обработчик кнопки "Надо исправить"
@router.callback_query(F.data == "user_edit_details")
async def user_edit_details(callback: types.CallbackQuery, state: FSMContext):

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
        state_message = await callback.message.edit_text(
            text=generate_requisites_message(platform)
        )

    await state.set_state(PaymentState.user_details)
    await state.update_data({"last_id_message": state_message.message_id})