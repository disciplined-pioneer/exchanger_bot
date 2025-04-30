from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.user_details import *
from bot.templates.user.exchange_confirmation import *
from bot.keyboards.partner.result_exchange import *

from db.models.models import ExchangeHistory


router = Router()


# Обработчик кнопки "Я оплатил" у партнёра
@router.callback_query(F.data == "confirm_cny_received")
async def confirm_cny_received(callback: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    id_exchange = int(data.get('id_exchange', ''))
    
    await callback.message.edit_text(exchange_completed_message)

    # Изменяем статус
    exchange_rate = await ExchangeHistory.get(id=id_exchange)
    await exchange_rate.update(
        status="exchange_completed"
    )