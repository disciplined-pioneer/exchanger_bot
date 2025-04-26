from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.bot import bot

from bot.templates.user.start import *
from bot.templates.user.request_details import *

from bot.keyboards.user.start import *
from bot.keyboards.user.request_details import *
from bot.keyboards.user.request_details import generate_partner_buttons


router = Router()


# Обработка "Выбрать партнёра" + "Нзад"
@router.callback_query(F.data == "select_partner")
@router.callback_query(F.data == "back_partner")
async def select_partner(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text("Выберите партнёра",
                                     reply_markup=await generate_partner_buttons())
    

# Обработка выбранного партнёры
@router.callback_query(F.data.startswith("partner_"))
async def handle_partner(callback: types.CallbackQuery, state: FSMContext):

    # Сюда попадут все partner_1, partner_2 и т.д.
    partner_number = callback.data.split("_")[1]
    await callback.message.edit_text(text=await get_partner_summary_text(partner_number),
                                     reply_markup=exchange_keyboard)
    
    await state.update_data({"partner_number": partner_number}) # Сохраняем id в стостояние
    

# Обработка кнопки "Совершить обмен"
@router.callback_query(F.data == "make_exchange")
async def make_exchange(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=types_exchange_text,
                                     reply_markup=exchange_methods_keyboard)


# Обработка кнопки "Совершить обмен"
@router.callback_query(F.data.startswith("exchange_"))
async def exchange(callback: types.CallbackQuery, state: FSMContext):

    # Запрашиваем у пользователя сумму
    currency = callback.data.split("_")[1].upper()  # Получаем валюту
    state_message = await callback.message.edit_text(text=f"Введите сумму в {currency}:")

    # Сохраняем данные в состоянии
    await state.update_data({
        "exchange_type": callback.data.replace("exchange_", ''),
        "last_id_message": state_message.message_id
    })
    
    # Переходим в состояние сохранения суммы
    await state.set_state(ExchangeStates.summ)


# Сохраняем сумму
@router.message(ExchangeStates.summ)
async def process_input(message: types.Message, state: FSMContext):

    try:

        await message.delete()
        text = message.text.replace(",", ".").strip()

        # Получаем данные из состояния
        data = await state.get_data()
        last_bot_message_id = data.get("last_id_message")  # Используем правильный ключ

        try:
            amount = float(text)
            if amount <= 0:
                # Если сумма отрицательная или 0, выводим сообщение
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text=incorrect_data[0]
                )
                return
        except ValueError:
            # Если введено не число
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=incorrect_data[1]
            )
            return

        # Извлекаем тип обмена и платформу
        exchange_type = data.get('exchange_type', '')
        currency = exchange_type.split('_')[0]
        platform = exchange_type.split('_')[1]  # alipay или wechat

        # Формируем текст для сообщения
        exchange_message = await format_exchange_message(
            sum=float(text),
            currency=currency,
            platform=platform
        )
        await state.update_data({"sum_amout": float(text)})

        # Изменяем сообщение с суммой и данными обмена
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text=exchange_message,
            reply_markup=confirm_exchange_keyboard
        )
    
    except:
        pass


# Подтверждение обмена
@router.callback_query(F.data == "start_exchange")
async def start_exchange(callback: types.CallbackQuery, state: FSMContext):

    # Сохраняем данные в состоянии
    state_message = await callback.message.edit_text(text=waiting_details)

    # Получаем текущие данные состояния
    data = await state.get_data()
    data.update({
        "tg_id": callback.message.from_user.id,
        "last_id_message": state_message.message_id
    })
    await state.update_data(data)

    # Отправляем сообщение нужному партнёру
    data = await state.get_data()
    sum_amount = data.get('sum_amout', 0)
    currency = data.get('exchange_type', '').split('_')[0].upper()

    partner_number = int(data.get('partner_number'))
    partner_id = settings.bot.PARTNERS[partner_number-1]
    await bot.send_message(partner_id, await format_exchange_request(amount=sum_amount, currency=currency))

# Вернуться в меню "Назад"
@router.callback_query(F.data == "back_menu")
async def back_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=starting_user_message, reply_markup=start_user_keyb)

