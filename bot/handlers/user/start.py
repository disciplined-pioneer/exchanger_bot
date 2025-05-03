from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.start import *
from bot.keyboards.user.start import *
from bot.templates.user.start import *


router = Router()


# Обработка входящих сообщений
@router.message(Command("start", ignore_case=True))
async def cmd_start(message: Message, state: FSMContext):

    # Удаляем всю историю сообщений
    data = await state.get_data()
    report_id = data["report"] if 'report' in data else message.message_id - 90
    try:
        await bot.delete_messages(message.chat.id,
                                    list(range(max(1, message.message_id - 90, report_id + 1), message.message_id + 1)))
    except Exception:
        pass

    
    # Проверка на бан пользователя
    tg_id = message.from_user.id
    result_ban_user, role_user = await check_ban_status(tg_id)
    if result_ban_user:
        await message.answer(text='❌ Ваш аккаунт был забанен')
        return


    #await message.answer(text=starting_user_message, reply_markup=start_user_keyb)

    if tg_id in settings.bot.ADMINS: # Админ
        await message.answer(
            text=starting_admin_message,
            reply_markup=start_admin_keyb
        )

    elif tg_id in settings.bot.PARTNERS: # Парнёр
        await message.answer(
            text=await get_exchange_rate(),
            reply_markup=await get_partner_menu(tg_id)
        )

    else: # Пользователь
        await message.answer(
            text=starting_user_message,
            reply_markup=start_user_keyb
        )

    await state.clear()
 