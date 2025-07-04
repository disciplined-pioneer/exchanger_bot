from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.exchange_currency import *
from bot.keyboards.user.exchange_currency import *
from bot.templates.user.exchange_currency import *

from settings import settings
from db.models.models import Exchanges
from db.models.mapped_columns import now_moscow


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

    # Отправляем сообщение
    keyboard, text = await buttons_with_all_ads(currency, platform)
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )

    await state.update_data(
        currency=currency,
        platform=platform
    )
    

# Обработка кнопки выбора партнёра
@router.callback_query(F.data.startswith("rate_id:"))
async def partner(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    currency = data.get('currency', '')
    platform = data.get('platform', '')
    id = int(callback.data.split(':')[1])

    text, partner_id = await partner_information(currency, id)
    await callback.message.edit_text(
        text=text,
        reply_markup=await keyboard_exchange_confirm(currency, platform)
    )

    await state.update_data(partner_id=partner_id, id_rates=id)


# Обработка кнопки "Совершить обмен"
@router.callback_query(F.data == "start_confirm_exchange")
async def start_confirm_exchange(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    currency = data.get('currency', '')
    id_rates = data.get('id_rates')

    text, limits = await confirmation_amount(currency, id_rates)
    msg = await callback.message.edit_text(
        text=text,
        reply_markup=back_menu
    )

    await state.update_data(
        last_id_message=msg.message_id,
        limits=limits
    )
    await state.set_state(ExchangeStates.sum)


# Сохраняем сумму
@router.message(ExchangeStates.sum)
async def process_input(message: types.Message, state: FSMContext):

    data = await state.get_data()
    currency = data.get("currency", '')
    platform = data.get("platform", '')
    id_rates = data.get("id_rates")
    partner_id = data.get('partner_id')

    limits = data.get("limits", '')
    limits_list = limits.split('-')
    limit_low = int(limits_list[0])
    limit_high = int(limits_list[1])

    last_bot_message_id = data.get("last_id_message", 0)

    try:

        await message.delete()
        text = message.text.replace(",", ".").strip()

        try:
            amount = float(text)
            if amount <= 0:
                # Если сумма отрицательная или 0, выводим сообщение
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text=incorrect_data[0],
                    reply_markup=back_menu
                )
                await state.set_state(ExchangeStates.sum)
                return
            
            # Проверка диапазона
            if not (limit_low <= amount <= limit_high):
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    text=incorrect_data[2] + limits,
                    reply_markup=back_menu
                )
                await state.set_state(ExchangeStates.sum)
                return
            
            # Если всё хорошо
            text, cny_sum = await format_exchange_message(amount, currency, platform, id_rates, partner_id)
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=text,
                reply_markup=confirm_cancel_exchange
            )
            await state.update_data(sum_amount=amount, cny_sum=cny_sum)
            await state.set_state(ExchangeStates.plug)
            return
            
        except ValueError:
            # Если введено не число
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
                text=incorrect_data[1],
                reply_markup=back_menu
            )
            return

    except:
        pass


# Обработка кнопки "Совершить обмен"
@router.callback_query(F.data == "confirm_exchange")
async def confirm_exchange(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Ожидайте реквизиты для оплаты!')

    # Получаем данные
    data = await state.get_data()
    tg_id = callback.from_user.id
    cny_sum = data.get('cny_sum', 0)
    partner_id = data.get('partner_id', 0)
    sum_amount = data.get('sum_amount', 0)
    currency = data.get('currency', '')
    platform = data.get('platform', '')

    # Сохраняем начало обмена в БД
    exchange = await Exchanges.create(
        client_id=tg_id,
        partner_id=partner_id,
        from_currency=currency,
        to_currency="CNY",
        amout_from=sum_amount,
        amout_to=cny_sum,
        platform=platform,
        state="NEW",
        created_at=now_moscow(),
        payment_check="None"
    )

    await state.update_data(id_exchange=exchange.id)

    # Отправляем сообщение нужному партнёру
    await bot.send_message(chat_id=partner_id,
                           text=await format_exchange_request(amount=sum_amount, currency=currency, platform=platform, cny_sum=cny_sum),
                           reply_markup=await send_details(tg_id))
    
    # Считываем состояние пользователя и переход в нужное состояние
    partner_state = FSMContext(
        storage=state.storage,
        key=state.key.__class__(bot_id=state.key.bot_id, chat_id=partner_id, user_id=partner_id)
    )
    await partner_state.set_state(ExchangeStates.partner_details)
    await partner_state.update_data(user_id=tg_id, id_exchange=exchange.id)
    await partner_state.update_data(**data)

    # Логгирование в группу
    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text=f"📝 Новая заявка от клиента {tg_id}. Направление: {currency} → CNY. Сумма: {sum_amount} {currency}"
    )


# Обработка кнопки "Назад"
@router.callback_query(F.data.startswith("go_back_exchange:"))
async def go_back_exchange(callback: types.CallbackQuery, state: FSMContext):

    #await exchange_currency(callback, state)

    type_back = callback.data.split(':')[1]
    if type_back == 'exchange_currency':
        await exchange_currency(callback, state)
    if type_back == 'type_exchange':
        await type_exchange(callback, state)