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

    print('🛑 Удаляем сообщение - не в состоянии 🛑')
    await message.delete()    
    

# Обработка кнопки "Назад" в меню
@router.callback_query(F.data == "go_back_menu")
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()

    tg_id = callback.from_user.id
    info_users = await Users.get(tg_id=tg_id)
    role = info_users.role
    
    try:
        # Убираем кнопки из старого сообщения, не меняя текст
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    if role == 'admin': # Админ
        await callback.message.answer(
            text=starting_admin_message,
            reply_markup=start_admin_keyb
        )

    elif role == 'partner': # Парнёр
        await callback.message.answer(
            text=starting_parner_message,
            reply_markup=await get_partner_menu(tg_id)
        )

    else: # Пользователь
        await callback.message.answer(
            text=starting_user_message,
            reply_markup=start_user_keyb
        )

    await state.clear()
