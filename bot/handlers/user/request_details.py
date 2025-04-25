from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.bot import bot
from settings import settings
from bot.keyboards.user.start import *
from bot.templates.user.start import *

from bot.keyboards.user.request_details import generate_partner_buttons


router = Router()


# Обработка "Выбрать партнёра"
@router.callback_query(F.data == "select_partner")
async def select_partner(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text("Выберите партнёра",
                                     reply_markup=await generate_partner_buttons())