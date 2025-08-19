from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from core.bot import bot

from bot.keyboards.partner.send_details import *
from bot.templates.partner.send_details import *

from settings import settings
from db.models.models import Exchanges
from utils.user.request_details import ExchangeStates


router = Router()


# Обработка кнопки "Отправить реквизиты"
@router.callback_query(F.data.startswith("send_details"))
async def send_details(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    ex_ids = data.get('ex_ids', {})

    user_id = callback.data.split('_')[1]
    ex_id = callback.data.split('_')[2]

    try:
        # Убираем кнопки из старого сообщения, не меняя текст
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # Отправляем новое сообщение с текстом для ввода реквизитов
    state_message = await callback.message.answer(input_requisites_message)

    ex_ids[user_id] = ex_id

    await state.set_state(ExchangeStates.details)
    await state.update_data(last_id_message=state_message.message_id, ex_ids=ex_ids)


# Сохраняем введённые реквизиты
@router.message(StateFilter(ExchangeStates.details), F.text)
async def save_details(message: types.Message, state: FSMContext):

    await message.delete()

    # Проверка на текст
    if not message.text:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=enter_requisites_message
            )
        except Exception as e:
            print(e)
            pass
        return

    details_text = message.text.strip()
    await state.update_data(details=details_text)

    try:

        # Отправляем новое сообщение с подтверждением
        new_message = await bot.send_message(
            chat_id=message.chat.id,
            text=get_confirm_requisites_message(details_text),
            reply_markup=confirm_details_keyboard
        )

        # Обновляем ID последнего сообщения
        await state.update_data(last_id_message=new_message.message_id)

    except Exception as e:
        print(e)

    await state.set_state(None)  # Снимаем состояние


# Обработка кнопки "Подтверждаю"
@router.callback_query(F.data == "confirm_details")
async def confirm_details(callback: types.CallbackQuery, state: FSMContext):
    
    await callback.answer()
    tg_id = callback.from_user.id
    partner_data = await state.get_data()
    user_id = partner_data.get('user_id', '')

    # Считываем состояние пользователя
    user_state = FSMContext(
        storage=state.storage,
        key=state.key.__class__(bot_id=state.key.bot_id, chat_id=user_id, user_id=user_id)
    )

    # Достаём данные пользователя
    user_data = await user_state.get_data()
    details = partner_data.get('details', '')
    sum_amount = user_data.get('sum_amount', '')
    currency = user_data.get('currency', '')
    id_exchange = user_data.get('id_exchange', '')

    # Удаляем клавиатуру у сообщения
    try:
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
    except:
        pass

    # Отправляем сообщение пользователю
    new_msg = await bot.send_message(
        chat_id=user_id,
        text=await create_payment_message(
            details=details,
            sum=sum_amount,
            currency=currency
        ),
        reply_markup=payment_keyboard
    )
    
    info_exchange = await Exchanges.get(id=id_exchange)
    await info_exchange.update(last_id_msg=new_msg.message_id)

    # Отправляем новое сообщение партнёру
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=requisites_sent_message
    )

    await state.update_data({'id_exchange': id_exchange})

    # Логгирование в группу
    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text=f"📤 Партнёр {tg_id} отправил реквизиты для оплаты по заявке {id_exchange}"
    )


# Отмена реквизитов (редактирование)
@router.callback_query(F.data == "edit_details")
async def edit_details(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    # Удаляем кнопки у старого сообщения
    try:
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=last_bot_message_id,
            reply_markup=None
        )
    except:
        pass

    # Отправляем новое сообщение с просьбой ввести реквизиты
    new_msg = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=input_requisites_message
    )

    # Обновляем состояние
    await state.set_state(ExchangeStates.details)
    await state.update_data(last_id_message=new_msg.message_id)
