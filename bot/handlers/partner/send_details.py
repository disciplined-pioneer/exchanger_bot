from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot

from bot.keyboards.partner.send_details import *
from bot.templates.partner.send_details import *

from settings import settings
from utils.user.request_details import ExchangeStates


router = Router()


# Обработка кнопки "Отправить реквизиты"
@router.callback_query(F.data.startswith("send_details"))
async def send_details(callback: types.CallbackQuery, state: FSMContext):

    state_message = await callback.message.edit_text(input_requisites_message)
    
    await state.set_state(ExchangeStates.details)
    await state.update_data({"last_id_message": state_message.message_id})


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

    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text=get_confirm_requisites_message(details_text),
            reply_markup=confirm_details_keyboard
        )
    except:
        pass

    await state.set_state(None)  # Снимаем состояние


# обработка кнопкии "Подтверждаю"
@router.callback_query(F.data == "confirm_details")
async def confirm_details(callback: types.CallbackQuery, state: FSMContext):

    tg_id = callback.from_user.id
    partner_data = await state.get_data()
    user_id = partner_data.get('user_id', '')

    # Считываем состояние пользователя
    user_state = FSMContext(
        storage=state.storage,
        key=state.key.__class__(bot_id=state.key.bot_id, chat_id=user_id, user_id=user_id)
    )
   
    # Отправляем реквизиты пользователю
    user_data = await user_state.get_data()
    details = partner_data.get('details', '')
    sum = user_data.get('sum_amount', '')
    currency = user_data.get('currency', '')

    await bot.send_message(
        chat_id=user_id,
        text=await create_payment_message(details=details,
                                          sum=sum,
                                          currency=currency),
        reply_markup=payment_keyboard
    )

    await callback.message.edit_text(text=requisites_sent_message)
    await state.update_data({'id_exchange': user_data.get('id_exchange', '')})

    # Логгирование в группу
    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text=f"📤 Партнёр {tg_id} отправил реквизиты для оплаты по заявке {user_data.get('id_exchange', '')}" 
    )


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


