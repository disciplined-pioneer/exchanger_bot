from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from bot.keyboards.partner.receiving_application import *
from bot.templates.user.request_details import ExchangeStates


router = Router()


# Обработка кнопки "Отправить реквизиты"
@router.callback_query(F.data.startswith("send_details"))
async def send_details(callback: types.CallbackQuery, state: FSMContext):

    tg_id = callback.data.split("_")[2]
    state_message = await callback.message.edit_text("Введите свои реквизиты:")
    await state.set_state(ExchangeStates.details)
    await state.update_data({"last_id_message": state_message.message_id,
                             "tg_id": tg_id})


# Сохраняем введённые реквизиты
@router.message(ExchangeStates.details)
async def save_details(message: types.Message, state: FSMContext):

    await message.delete()
    details_text = message.text.strip()
    await state.update_data(details=details_text)

    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=last_bot_message_id,
        text=f"Подтвердите реквизиты:\n\n{details_text}",
        reply_markup=confirm_details_keyboard
    )

    print(data)


# обработка кнопкии "Подтверждаю"



# Отмена реквизитов
@router.callback_query(F.data == "edit_details")
async def edit_details(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    last_bot_message_id = data.get("last_id_message")

    state_message = await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=last_bot_message_id,
        text="Введите свои реквизиты:"
    )

    await state.set_state(ExchangeStates.details)
    await state.update_data({"last_id_message": state_message.message_id})
