from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from settings import settings
from utils.user.user_details import *

from bot.templates.user.user_details import *
from bot.keyboards.user.user_details import *



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
        caption="Подтвердите отправку реквизитов (фото):"
    elif message.document:
        caption=f"Подтвердите отправку реквизитов (документ)"
    elif message.text:
        caption=f"Подтвердите реквизиты: {message.text}"

    sent_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=last_bot_message_id,
        text=caption,
        reply_markup=user_confirm_keyb
    )

    # Сохраняем новое сообщение для трекинга
    await state.update_data({"last_id_message": sent_message.message_id})


# Обработчик кнопки "Надо исправить"
@router.callback_query(F.data == "user_edit_details")
async def user_edit_details(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    exchange_type = data.get('exchange_type', '').split('_')[1].capitalize()
    state_message = await callback.message.edit_text(generate_requisites_message(exchange_type))

    await state.set_state(PaymentState.user_details)
    await state.update_data({"last_id_message": state_message.message_id})