from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.bot import bot
from settings import settings

from bot.templates.user.start import *
from bot.templates.user.request_details import *

from bot.keyboards.user.start import *
from bot.keyboards.user.request_details import *
from bot.keyboards.user.request_details import generate_partner_buttons


router = Router()


# Обработка "Выбрать партнёра" + "Нзад"
@router.callback_query(F.data == "select_partner")
@router.callback_query(F.data == "back_partner")
async def select_partner(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text("Выберите партнёра",
                                     reply_markup=await generate_partner_buttons())
    

# Обработка выбранного партнёры
@router.callback_query(F.data.startswith("partner_"))
async def handle_partner(callback: types.CallbackQuery, state: FSMContext):

    # Сюда попадут все partner_1, partner_2 и т.д.
    partner_id = callback.data.split("_")[1]
    await callback.message.edit_text(text=await get_partner_summary_text(partner_id),
                                     reply_markup=exchange_keyboard)
    
    await state.set_data({"partner_id": partner_id}) # Сохраняем id в стостояние
    

# Обработка кнопки "Совершить обмен"
@router.callback_query(F.data == "make_exchange")
async def make_exchange(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=types_exchange_text,
                                     reply_markup=exchange_methods_keyboard)


# Вернуться в меню "Назад"
@router.callback_query(F.data == "back_menu")
async def back_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=starting_user_message, reply_markup=start_user_keyb)

