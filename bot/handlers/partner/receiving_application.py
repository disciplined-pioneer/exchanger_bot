from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from bot.keyboards.partner.receiving_application import *
from bot.templates.partner.receiving_application import *
from utils.user.request_details import ExchangeStates


router = Router()


# Обработка кнопки "Отправить реквизиты"
@router.callback_query(F.data.startswith("send_details"))
async def send_details(callback: types.CallbackQuery, state: FSMContext):

    tg_id = callback.data.split("_")[2]
    state_message = await callback.message.edit_text(input_requisites_message)
    await state.set_state(ExchangeStates.details)
    await state.update_data({"last_id_message": state_message.message_id,
                             "tg_id": tg_id})


# Сохраняем введённые реквизиты
@router.message(ExchangeStates.details)
async def save_details(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    # Проверка на текст
    try:
        if not message.text:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=enter_requisites_message
            )
            return
    except:
        pass
        return
    
    details_text = message.text.strip()
    await state.update_data(details=details_text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=last_bot_message_id,
        text=get_confirm_requisites_message(details_text),
        reply_markup=confirm_details_keyboard
    )


# обработка кнопкии "Подтверждаю"
@router.callback_query(F.data == "confirm_details")
async def confirm_details(callback: types.CallbackQuery, state: FSMContext):

    partner_data = await state.get_data()
    tg_id = int(partner_data.get('tg_id', ''))

    # Считываем состояние пользователя
    user_state = FSMContext(
        storage=state.storage,
        key=state.key.__class__(bot_id=state.key.bot_id, chat_id=tg_id, user_id=tg_id)
    )
   
    # Отправляем реквизиты
    user_data = await user_state.get_data()
    details = partner_data.get('details', '')
    sum = user_data.get('sum_amout', '')
    currency = user_data.get('exchange_type', '').split('_')[0].upper()
    await bot.send_message(
        chat_id=tg_id,
        text=await create_payment_message(details=details,
                                          sum=sum,
                                          currency=currency),
        reply_markup=payment_keyboard
    )

    await callback.message.edit_text(text=requisites_sent_message)
    await state.update_data({'id_exchange': user_data.get('id_exchange', '')})


# Отмена реквизитов
@router.callback_query(F.data == "edit_details")
async def edit_details(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    state_message = await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=last_bot_message_id,
        text=input_requisites_message
    )

    await state.set_state(ExchangeStates.details)
    await state.update_data({"last_id_message": state_message.message_id})
