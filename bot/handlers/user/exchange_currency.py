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
    
    await state.clear()
    await callback.message.edit_text(
        text=await display_available_exchanges(),
        reply_markup=await output_all_possible_exchanges()
    )


# Обработка кнопки выбора направления
@router.callback_query(F.data.startswith("type_exchange:"))
async def type_exchange(callback: types.CallbackQuery, state: FSMContext):

    # Если мы вернулиьсь с помощью "Назад"
    data = await state.get_data()
    currency = data.get('currency', '')
    platform = data.get('platform', '')

    if currency == '' and platform == '':
        
        # Получаем данные из кноки
        type_exchange = callback.data.split(':')[1]
        currency = type_exchange.split('_')[0].upper()
        platform = type_exchange.split('_')[1].capitalize()


    await callback.message.edit_text(
        text='Выберите объявление',
        reply_markup=await buttons_with_all_ads(currency, platform)
    )

    #await state.set_state(PaymentState.user_details)
    await state.update_data(
        currency=currency,
        platform=platform
    )
    

# Обработка кнопки выбора партнёра
@router.callback_query(F.data.startswith("partner_id:"))
async def partner_id(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    currency = data.get('currency', '')
    platform = data.get('platform', '')
    partner_id = int(callback.data.split(':')[1])

    await callback.message.edit_text(
        text=await partner_information(currency, platform, partner_id),
        reply_markup=await keyboard_exchange_confirm(currency, platform)
    )

    await state.update_data(partner_id=partner_id)


# Обработка кнопки "Назад"
@router.callback_query(F.data.startswith("go_back_exchange:"))
async def go_back_exchange(callback: types.CallbackQuery, state: FSMContext):

    #await exchange_currency(callback, state)

    type_back = callback.data.split(':')[1]
    if type_back == 'exchange_currency':
        await exchange_currency(callback, state)
    if type_back == 'type_exchange':
        await type_exchange(callback, state)