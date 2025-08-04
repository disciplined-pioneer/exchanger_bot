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
    
    # Проверка на бан пользователя
    tg_id = message.from_user.id
    result_ban_user, role_user = await check_ban_status(tg_id)
    if result_ban_user:
        await message.answer(text='❌ Ваш аккаунт был забанен')
        return
    
    # Ищем уже активные сделки
    all_exchanges = await Exchanges.exclude(state=['CANCELLED', 'COMPLETED'])
    if all_exchanges:
        await message.delete()
        await message.answer(there_deal_message)
        return

    #await message.answer(text=starting_user_message, reply_markup=start_user_keyb)

    if role_user == 'admin': # Админ
        await message.answer(
            text=starting_admin_message,
            reply_markup=start_admin_keyb
        )

    elif role_user == 'partner': # Парнёр
        await message.answer(
            text=starting_parner_message,
            reply_markup=await get_partner_menu(tg_id)
        )

    else: # Пользователь
        await message.answer(
            text=starting_user_message,
            reply_markup=start_user_keyb
        )

    await message.delete()