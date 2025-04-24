from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db.models.models import UserTopics

from core.bot import bot
from utils.start import *
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
        

# Обрабатываем "О нас"
@router.callback_query(F.data == "info_about_us")
async def show_price_list(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=info_about_text,
        reply_markup=submit_request_keyboard
    )
    await callback.answer()


# Обрабатываем "Цены"
@router.callback_query(F.data == "price_list")
async def show_price_list(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=price_info_text,
        reply_markup=submit_request_keyboard
    )
    await callback.answer()


# Обрабатываем "Оставить заявку"
@router.callback_query(F.data == "submit_request")
async def show_price_list(callback: types.CallbackQuery):

    # Если нет заявки
    result = await UserTopics.get_by_tg_id(callback.from_user.id)
    if not result:
        topic_id = await create_topic(callback.from_user)
        await callback.message.edit_text(
            text=success_message,
            reply_markup=None
        )
        return
    
    # Если есть заявка
    await callback.message.edit_text(
        text=already_sent_message,
        reply_markup=None
    )

    await callback.answer()


# Обработка кнопки "Назад" к старту
@router.callback_query(F.data == "back_start")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.edit_text(text=starting_message, reply_markup=start_keyboard)