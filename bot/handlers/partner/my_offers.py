from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from db.models.models import Rates

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
    tg_id = callback.from_user.id
    await callback.message.edit_text(
        text=choose_ad_message,
        reply_markup=await build_rates_keyboard_for_partner(tg_id)
    )


# Обработка кнопки "Выбора курса"
@router.callback_query(F.data.startswith('rate:'))
async def rate(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    rate_id = int(callback.data.split(':')[1])
    rate_info = await Rates.get(id=rate_id)

    await callback.message.edit_text(
        text=get_rate_info_text(rate_info),
        reply_markup=await actions_with_course(rate_id)
    )


# Обработка кнопки удаления курса
@router.callback_query(F.data.startswith('delete_rate:'))
async def delete_rate(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    rate_id = int(callback.data.split(':')[1])
    rate = await Rates.get(id=rate_id)
    if rate:
        await rate.delete()
        await callback.message.edit_text(
            text=rate_deleted_message,
            reply_markup=back_menu
        )
    else:
        await callback.message.edit_text(
            text=rate_not_found_message,
            reply_markup=back_menu
        )


# Обработка кнопки редактирования курса
@router.callback_query(F.data.startswith('edit_rate:'))
async def edit_rate(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    rate_id = int(callback.data.split(':')[1])
    rate = await Rates.get(id=rate_id)

    msg = await callback.message.edit_text(
        text=get_payment_prompt(rate),
        reply_markup=back_menu_rate("edit")
    )

    await state.update_data(
        rate_id=rate_id,
        last_bot_message_id=msg.message_id
    )
    await state.set_state(RateEdit.rate)


# Сохраняем введённый курс
@router.message(RateEdit.rate)
async def save_rate(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    rate_id = data.get('rate_id', 0)
    last_bot_message_id = data.get('last_bot_message_id', 0)
    new_rate = message.text.replace(",", ".")

    result, text_error = validate_exchange_rate(new_rate)
    try:
        if not result:
            msg = await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_bot_message_id,
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

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=last_bot_message_id,
        text=rate_updated_message,
        reply_markup=back_menu
    )

    await state.clear()


# Универсальная обработка кнопки "Назад" с context'ом
@router.callback_query(F.data.startswith("go_back_rate:"))
async def go_back_rate(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    context = callback.data.split(":")[1]
    if context == "rates_list":
        tg_id = callback.from_user.id
        await callback.message.edit_text(
            text=choose_ad_message,
            reply_markup=await build_rates_keyboard_for_partner(tg_id)
        )
        await state.clear()

    elif context == "edit":
        data = await state.get_data()
        rate_id = data.get('rate_id', 0)
        rate_info = await Rates.get(id=rate_id)

        await callback.message.edit_text(
            text=get_rate_info_text(rate_info),
            reply_markup=await actions_with_course(rate_id)
        )
        await state.clear()
