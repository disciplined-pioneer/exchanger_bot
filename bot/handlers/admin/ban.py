from core.bot import bot
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from utils.admin.ban import *
from bot.keyboards.admin.ban import *
from bot.templates.admin.ban import *

from db.models.models import Users


router = Router()

import time
# Обработка бана пользователя
@router.callback_query(F.data == "ban_user")
async def start_ban_user(callback: types.CallbackQuery, state: FSMContext):

    state_message = await callback.message.edit_text(
        text=telegram_id_message,
        reply_markup=back_keyb
    )

    await state.update_data({"last_bot_message_id": state_message.message_id})
    await state.set_state(UserBan.tg_id)


# Обработка бана по id
@router.message(UserBan.tg_id)
async def process_ban(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    last_bot_message_id = data.get('last_bot_message_id', 0)

    # Обработка неправильного ID
    text = message.text
    if not text.isdigit() or int(text) <= 0:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=telegram_id_error_message,
                reply_markup=back_keyb
            )
        except:
            pass
        return
    
    # Для тех, кто уже есть в БД
    value = int(text)
    user = await Users.get(tg_id=value, role='ban')
    if user: # Если бан уже стоит
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=partner_id_exists_message,
                reply_markup=back_keyb
            )
        except:
            pass
        return
    
    user = await Users.get(tg_id=value)
    if user: # Если пользователь найден, обновляем его роль
        await user.update(role='ban')

    else: # Если пользователь не найден, создаем новой с ролью 'ban'
        await Users.create(tg_id=value, role='ban')

    # Выводим результат
    await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text=user_banned_message(value),
            reply_markup=back_menu_keyb
        )

    await state.clear()