from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from bot.keyboards.partner.create_offer import *
from bot.templates.partner.create_offer import *
from bot.keyboards.partner.currency_rate_update import back_menu

from utils.partner.create_offer import *



router = Router()


# Обработка кнопки "Создать объявление"
@router.callback_query(F.data == "create_offer")
async def create_offer(callback: types.CallbackQuery, state: FSMContext):

    tg_id = callback.from_user.id
    await callback.message.edit_text(
        text=direction_input,
        reply_markup=await currency_keyboard(tg_id)
    )
    await state.set_state(CollectingCurrencyInfo.start)


# Выбор направления
@router.callback_query(F.data.startswith("change_value_"))
async def change_value(callback: types.CallbackQuery, state: FSMContext):

    callback_data = callback.data[len("change_value_"):].split('_')
    platform = callback_data[0].capitalize()
    currency = callback_data[1].upper()
    
    msg = await callback.message.edit_text(
        text=generate_announcement_message(platform, currency),
        reply_markup=create_offer_back_keyb
    )

    await state.set_data({'platform': platform, 'currency': currency})
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(CollectingCurrencyInfo.range_limits)

    await callback.answer()


# Обработка ввода диапазона
@router.message(CollectingCurrencyInfo.range_limits)
async def range_limits(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    currency = data.get('currency', '')
    last_bot_message_id = data.get('last_bot_message_id', 0)

    # Проверка на корректное значение диапазона
    result, text_error = validate_limits_input(message.text)
    try:
        if not result:
            msg = await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=text_error,
                reply_markup=create_offer_back_keyb
            )
            await state.update_data(last_bot_message_id=msg.message_id)
            return
    except:
        return

    # Обновляем сообщение бота
    try:
        msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text=exchange_rate_message(currency),
            reply_markup=create_offer_back_keyb
        )
        await state.update_data(last_bot_message_id=msg.message_id)
    except Exception as e:
        print(f"Не удалось отредактировать сообщение: {e}")
    
    # Обновляем состояние
    await state.update_data(
        limits=message.text
    )
    await state.set_state(CollectingCurrencyInfo.exchange_rate)


# Обработка ввода диапазона
@router.message(CollectingCurrencyInfo.exchange_rate)
async def range_limits(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    platform = data.get('platform', '')
    currency = data.get('currency', '')
    limits = data.get('limits', '')
    exchange_rate = message.text.replace(",", ".")
    last_bot_message_id = data.get('last_bot_message_id', 0)

    # Проверка на корректное значение валюты
    result, text_error = validate_exchange_rate(exchange_rate)
    try:
        if not result:
            msg = await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=text_error,
                reply_markup=create_offer_back_keyb
            )
            await state.update_data(last_bot_message_id=msg.message_id)
            return
    except:
        return
    
    
    # Добавляем в БД и удаляем, если запись уже есть
    await save_rate(currency, exchange_rate, platform, limits, message.from_user.id)
    
    
    msg = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=last_bot_message_id,
        text=create_advertisement_message(platform, currency, limits, exchange_rate),
        reply_markup=back_menu
    )
 
    await state.clear()


# Обработка кнопки "Назад"
@router.callback_query(F.data == "create_offer_go_back")
async def create_offer_go_back(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    current_state = await state.get_state()

    # Переходы к предыдущим состояниям
    if current_state == CollectingCurrencyInfo.range_limits.state:
        await state.set_state(CollectingCurrencyInfo.start)
        await callback.message.edit_text(
            text=direction_input,
            reply_markup=await currency_keyboard(callback.from_user.id)
        )
        await callback.answer()

    elif current_state == CollectingCurrencyInfo.exchange_rate.state:
        platform = data.get('platform', '')
        currency = data.get('currency', '')
        await state.set_state(CollectingCurrencyInfo.range_limits)
        await callback.message.edit_text(
            text=generate_announcement_message(platform, currency),
            reply_markup=create_offer_back_keyb
        )
        await callback.answer()