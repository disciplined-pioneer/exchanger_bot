from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.bot import bot
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

    await message.answer(text=starting_message, reply_markup=start_keyboard)
        