from core.bot import bot
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from utils.partner.currency_rate_update import *
from bot.templates.user.start import get_exchange_rate
from bot.keyboards.user.start import update_rate_keyb
from bot.keyboards.partner.currency_rate_update import *

from db.models.models import ExchangeRate


router = Router()


# Обработка кнопки "Обновить курс"
@router.callback_query(F.data == "update_rate_partner")
async def start_update(callback: types.CallbackQuery, state: FSMContext):

    # Инициализация состояния
    await callback.message.delete()
    await state.set_data({"index": 0, "values": {}})
    await state.set_state(UpdateRates.current_index)

    await ask_next(callback.message, state)
    await callback.answer()


# Сохранение данных и изменение индекса
@router.message(UpdateRates.current_index)
async def process_input(message: types.Message, state: FSMContext):

    # Удаляем сообщение пользователя сразу после получения
    await message.delete()

    # Получаем данные состояния
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")

    try:
        value = float(message.text.replace(",", "."))
        if value <= 0:
            try:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text="❌ Число должно быть положительным!",
                    reply_markup=back_keyboard()
                )
            except:
                pass
            return

    except ValueError:
        # Если значение не корректное — редактируем старое сообщение с ошибкой
        if last_bot_message_id:
            try:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text="❌ Введите число!",
                    reply_markup=back_keyboard()
                )
            except:
                pass
        return
    except:
        pass

    keys = list(LIST_CURRENCIES.keys())
    current_key = keys[data["index"]]

    data["values"][current_key] = value
    data["index"] += 1
    await state.set_data(data)

    await ask_next(message, state)


# Переход к следующему вопросу
async def ask_next(message: types.Message, state: FSMContext):

    # Получаем данные состояния
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")

    index = data["index"]
    keys = list(LIST_CURRENCIES.keys())

    # Если вопросы закончились — уведомляем и завершаем
    if index >= len(keys):
        await state.set_state(UpdateRates.values)
        if last_bot_message_id:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text="✅ Курс валют был изменён!"
            )
        
        # Изменяем курс
        values = data.get('values', {})
        exchange_rate = await ExchangeRate.get(id=1)
        await exchange_rate.update(usdt_alipay=values.get('usdt_alipay', 0.0),
                                  usdt_wechat=values.get('usdt_wechat', 0.0),
                                  rub_alipay=values.get('rub_alipay', 0.0),
                                  rub_wechat=values.get('rub_wechat', 0.0))
        await state.clear()
        return

    # Получаем текущий вопрос
    current_key = keys[index]
    question = LIST_CURRENCIES[current_key]

    # Если last_bot_message_id существует, редактируем старое сообщение
    if last_bot_message_id:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text=question,
            reply_markup=back_keyboard()
        )
    else:
        # Если last_bot_message_id нет, отправляем новое сообщение
        sent_message = await message.answer(question, reply_markup=back_keyboard())
        await state.update_data(last_bot_message_id=sent_message.message_id)


# Обработка кнопки "Назад"
@router.callback_query(F.data == "go_back")
async def go_back(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data["index"] > 0:
        data["index"] -= 1
        keys = list(LIST_CURRENCIES.keys())
        current_key = keys[data["index"]]
        # Если курс уже был введён — удалить его
        if current_key in data["values"]:
            del data["values"][current_key]
        await state.set_data(data)
        await ask_next(callback.message, state)
    else:
        await callback.message.delete()
        await callback.message.answer(text=await get_exchange_rate(), reply_markup=update_rate_keyb)
        await state.clear()
    await callback.answer()