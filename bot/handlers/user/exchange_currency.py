from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.exchange_currency import *
from bot.keyboards.user.exchange_currency import *
from bot.templates.user.exchange_currency import *


router = Router()


# Обработка кнопки "Обменять валюту"
@router.callback_query(F.data == "exchange_currency")
async def exchange_currency(callback: types.CallbackQuery, state: FSMContext):

    
    await callback.message.edit_text(
        text=await display_available_exchanges(),
        reply_markup=await output_all_possible_exchanges()
    )