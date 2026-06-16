from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from db.models.models import Rates, Partners

from core.bot import bot
from bot.keyboards.partner.my_offers import *
from bot.templates.partner.my_offers import *

from utils.partner.my_offers import *
from utils.partner.create_offer import validate_exchange_rate 


router = Router()


# Обработка кнопки "Мои объявления"
@router.callback_query(F.data == "my_offers")
async def my_offers(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()

    try:
        # Убираем кнопки из старого сообщения, не меняя текст
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    tg_id = callback.from_user.id
    partner_info = await Partners.get(tg_id=tg_id)

    # Отправляем новое сообщение с текстом и клавиатурой
    await callback.message.answer(
        text=choose_ad_message,
        reply_markup=await build_rates_keyboard_for_partner(partner_info.id)
    )


# Обработка кнопки "Выбора курса"
@router.callback_query(F.data.startswith('rate:'))
async def rate(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    rate_id = int(callback.data.split(':')[1])
    rate_info = await Rates.get(id=rate_id)

    # Убираем кнопки из старого сообщения, не меняя текст
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # Отправляем новое сообщение с информацией о курсе и клавиатурой действий
    await callback.message.answer(
        text=get_rate_info_text(rate_info),
        reply_markup=await actions_with_course(rate_id)
    )


# Обработка кнопки удаления курса
@router.callback_query(F.data.startswith('delete_rate:'))
async def delete_rate(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    rate_id = int(callback.data.split(':')[1])
    rate = await Rates.get(id=rate_id)

    # Убираем кнопки из старого сообщения, не меняя текст
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    if rate:
        await rate.delete()
        await callback.message.answer(
            text=rate_deleted_message,
            reply_markup=back_menu
        )
    else:
        await callback.message.answer(
            text=rate_not_found_message,
            reply_markup=back_menu
        )


# Обработка кнопки редактирования курса
@router.callback_query(F.data.startswith('edit_rate:'))
async def edit_rate(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    rate_id = int(callback.data.split(':')[1])
    rate = await Rates.get(id=rate_id)

    # Убираем кнопки из старого сообщения, не меняя текст
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # Отправляем новое сообщение с запросом оплаты и клавиатурой "назад"
    msg = await callback.message.answer(
        text=get_payment_prompt(rate),
        reply_markup=back_menu_rate("edit")
    )

    await state.update_data(
        rate_id=rate_id,
        last_bot_message_id=msg.message_id
    )
    await state.set_state(RateEdit.rate)


# Сохраняем введённый курс
@router.message(StateFilter(RateEdit.rate), F.text)
async def save_rate(message: types.Message, state: FSMContext):
    
    await message.delete()
    data = await state.get_data()
    rate_id = data.get('rate_id', 0)
    last_bot_message_id = data.get('last_bot_message_id', 0)
    new_rate = message.text.replace(",", ".")

    result, text_error = validate_exchange_rate(new_rate)
    try:
        if not result:
            # Убираем кнопки из старого сообщения, не меняя текста
            try:
                await bot.edit_message_reply_markup(
                    chat_id=message.chat.id,
                    message_id=last_bot_message_id,
                    reply_markup=None
                )
            except:
                pass
            # Отправляем новое сообщение с ошибкой и клавиатурой "назад"
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=text_error,
                reply_markup=back_menu_rate("edit")
            )
            await state.update_data(last_bot_message_id=msg.message_id)
            return
    except:
        return

    new_rate = float(new_rate)
    rate_info = await Rates.get(id=rate_id)
    await rate_info.update(rate=new_rate)

    # Убираем кнопки из старого сообщения, не меняя текста
    try:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            reply_markup=None
        )
    except:
        pass

    # Отправляем новое сообщение с подтверждением и кнопками
    await bot.send_message(
        chat_id=message.chat.id,
        text=rate_updated_message,
        reply_markup=back_menu
    )

    await state.clear()


# Универсальная обработка кнопки "Назад" с context'ом
@router.callback_query(F.data.startswith("go_back_rate:"))
async def go_back_rate(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    context = callback.data.split(":")[1]

    # Удаляем inline-кнопки у старого сообщения
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    if context == "rates_list":
        tg_id = callback.from_user.id
        new_msg = await callback.message.answer(
            text=choose_ad_message,
            reply_markup=await build_rates_keyboard_for_partner(tg_id)
        )
        await state.clear()

    elif context == "edit":
        data = await state.get_data()
        rate_id = data.get('rate_id', 0)
        rate_info = await Rates.get(id=rate_id)

        new_msg = await callback.message.answer(
            text=get_rate_info_text(rate_info),
            reply_markup=await actions_with_course(rate_id)
        )
        await state.clear()
