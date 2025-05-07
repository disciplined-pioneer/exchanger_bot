from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils.user.start import *
from bot.keyboards.user.start import *
from bot.templates.user.start import *

from bot.handlers.user.start import cmd_start


router = Router()


# Удаление сообщений, не подключённых к состоянию
@router.message()
async def handle_unexpected_message(message: types.Message, state: FSMContext):
    
    if message.text == '/start':
        await cmd_start(message, state)
        return
    
    current_state = await state.get_state()
    await message.delete()    
    

# Обработка кнопки "Назад" в меню
@router.callback_query(F.data == "go_back_menu")
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):

    tg_id = callback.from_user.id
    info_users = await Users.get(tg_id=tg_id)
    role = info_users.role

    if role == 'admin': # Админ
        await callback.message.edit_text(
            text=starting_admin_message,
            reply_markup=start_admin_keyb
        )

    elif role == 'partner': # Парнёр
        await callback.message.edit_text(
            text=starting_parner_message,
            reply_markup=await get_partner_menu(tg_id)
        )

    else: # Пользователь
        await callback.message.edit_text(
            text=starting_user_message,
            reply_markup=start_user_keyb
        )

    await state.clear()
    await callback.answer()