from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from db.models.models import Exchanges
from utils.user.user_details import *
from bot.templates.partner.view_requests import *
from bot.keyboards.partner.view_requests import *


router = Router()
    

# Обработчик кнопки "Заявки"
@router.callback_query(F.data == "view_requests")
async def view_requests(callback: types.CallbackQuery, state: FSMContext):

    partner_id = callback.from_user.id
    await callback.message.edit_text(
        text=choose_request_message,
        reply_markup=await get_partner_exchanges_keyboard(partner_id)
    )
    await callback.answer()


# Обновляем сообщение с новой клавиатурой
@router.callback_query(F.data.startswith('exchanges_next:'))
@router.callback_query(F.data.startswith('exchanges_prev:'))
async def next_page(call: types.CallbackQuery, state: FSMContext):

    page = int(call.data.split(":")[1])
    keyboard = await get_partner_exchanges_keyboard(partner_id=call.from_user.id, page=page)
    await call.message.edit_reply_markup(reply_markup=keyboard)


# Обработчик кнопки вида заявки 
@router.callback_query(F.data.startswith('exchange:'))
async def exchange(callback: types.CallbackQuery, state: FSMContext):

    # Получаем всю информацию
    exchanges_id = int(callback.data.split(':')[1])
    info_exchanges = await Exchanges.get(id=exchanges_id)
    platform = info_exchanges.platform 
    from_currency = info_exchanges.from_currency
    to_currency = info_exchanges.to_currency
    amount_from = info_exchanges.amout_from
    amount_to = info_exchanges.amout_to
    state = info_exchanges.state

    # Редактируем текст
    await callback.message.edit_text(
        text=get_transaction_details(platform, from_currency, to_currency, amount_to, amount_from, state),
        reply_markup=back_menu
    )