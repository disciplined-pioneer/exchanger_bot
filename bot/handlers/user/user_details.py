from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from core.bot import bot
from settings import settings
from bot.keyboards.user.user_details import *
from utils.user.user_details import *


router = Router()


# Обработчик кнопки "Я оплатил"
@router.callback_query(F.data == "payment_confirmed")
async def payment_confirmed(callback: types.CallbackQuery, state: FSMContext):
    state_message = await callback.message.edit_text("Пожалуйста, отправьте фото или файл с чеком в этот чат")
    await state.set_state(PaymentState.waiting_for_receipt)  # Переходим в состояние ожидания файла
    await state.update_data({"last_id_message": state_message.message_id})


# Обработчик для получения фото или файла
@router.message(PaymentState.waiting_for_receipt)  # Только для этого состояния
async def handle_receipt(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    try:
        partner_number = int(data.get('partner_number', '')) - 1
        partner_id = settings.bot.PARTNERS[partner_number]

        if message.photo:
            sent_file = message.photo[-1]  # Выбираем максимальный размер фото
            file_id = sent_file.file_id
            await state.update_data({"file_check": file_id})
            await bot.send_photo(partner_id, file_id, caption="Клиент подтвердил оплату и отправил чек:")

        elif message.document:
            file_id = message.document.file_id
            await state.update_data({"file_check": file_id})
            await bot.send_document(partner_id, file_id, caption="Клиент подтвердил оплату и отправил чек:")

        else:
            state_message = await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text="❗️ Пожалуйста, отправьте фото или документ"
            )
            await state.update_data({"last_id_message": state_message.message_id})
            return

        # Сообщение пользователю
        exchange_type = data.get('exchange_type', '').split('_')[1].capitalize()
        state_message = await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text=f"Введите свои реквизиты:\n{exchange_type}. Или загрузите QR-код для оплаты"
                )
        await state.update_data({"last_id_message": state_message.message_id})
        await state.set_state(PaymentState.user_details)
        

    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        pass


# Обработчик для получения реквизитов пользователя
@router.message(PaymentState.user_details)  # Только для этого состояния
async def user_details(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    state_message = await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text=f'Подтвердите реквизиты: {message.text}',
                    reply_markup=user_confirm_keyb
                )
    await state.update_data({"last_id_message": state_message.message_id})

    
