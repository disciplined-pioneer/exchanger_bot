from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from core.bot import bot

from utils.admin.add_partner import *
from bot.keyboards.user.start import start_admin_keyb
from bot.keyboards.admin.add_partner import back_admin_keyb
from bot.keyboards.partner.currency_rate_update import back_menu
from bot.templates.user.start import starting_admin_message

from db.models.models import Partners, Users


router = Router()


# Старт добавления партнёра
@router.callback_query(F.data == "add_partner")
async def start_add(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.set_data({"index": 0, "values": {}})
    await state.set_state(AddPartner.current_index)

    await ask_next(callback.message, state)
    await callback.answer()


# Обработка ответа на вопрос
@router.message(AddPartner.current_index)
async def process_input(message: types.Message, state: FSMContext):

    # Получение данных
    await message.delete()
    data = await state.get_data()
    index = data.get("index", 0)
    last_bot_message_id = data.get("last_bot_message_id")

    key = list(PARTNER_QUESTIONS.keys())[index]
    text = message.text.strip()

    # Валидация Telegram ID
    if key == "telegram_id":

        # Проверка на число
        if not text.isdigit() or int(text) <= 0:
            try:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text="❌ Telegram ID должен быть положительным числом!",
                    reply_markup=back_admin_keyb
                )
            except:
                pass
            return
        
        # Для тех, кто уже есть в БД
        value = int(text)
        user = await Partners.get(tg_id=value)
        if user:
            try:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text="❌ Партнёр с этиим ID уже существует, введите другой ID",
                    reply_markup=back_admin_keyb
                )
            except:
                pass
            return
    else:
        value = text

    # Сохранение вопроса и переход к следующему
    data["values"][key] = value
    data["index"] += 1
    await state.set_data(data)
    await ask_next(message, state)


# Переход к следующему вопросу или завершение
async def ask_next(message: types.Message, state: FSMContext):

    data = await state.get_data()
    index = data["index"]
    keys = list(PARTNER_QUESTIONS.keys())

    # Проверка на конечный результат
    if index >= len(keys):

        await state.set_state(AddPartner.values)
        values = data.get('values', {})
        name = values.get('name', '')
        telegram_id = values.get('telegram_id', 0)

        # Сохранение в БД
        await Users.create(
            tg_id=telegram_id,
            role='partner'
        )

        # Сохранение в БД
        await Partners.create(
            tg_id=telegram_id,
            name=name,
            active_pairs=[{'from': 'USDT', 'to': 'CNY'},
                          {'from': 'RUB', 'to': 'CNY'}]
        )

        
        # Отправляем сообщение
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["last_bot_message_id"],
            text=f"✅ Партнёр <b>{name}</b> был добавлен!",
            reply_markup=back_menu
        )

        await state.clear()
        return

    # Проверка
    question = PARTNER_QUESTIONS[keys[index]]
    if "last_bot_message_id" in data:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["last_bot_message_id"],
            text=question,
            reply_markup=back_admin_keyb
        )
    else:
        msg = await message.answer(question, reply_markup=back_admin_keyb)
        await state.update_data(last_bot_message_id=msg.message_id)


# Обработка кнопки "Назад"
@router.callback_query(F.data == "go_back_admin")
async def go_back(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0)

    if index > 0:
        data["index"] -= 1
        key = list(PARTNER_QUESTIONS.keys())[data["index"]]
        data["values"].pop(key, None)
        await state.set_data(data)
        await ask_next(callback.message, state)
    else:
        await callback.message.delete()
        await callback.message.answer(starting_admin_message, reply_markup=start_admin_keyb)
        await state.clear()

    await callback.answer()
