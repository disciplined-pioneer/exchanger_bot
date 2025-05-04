from aiogram import Router, F, types

from bot.keyboards.user.start import get_partner_menu
from bot.templates.user.start import starting_parner_message

from bot.templates.partner.statistics import *
from bot.keyboards.partner.statistics import back_menu


router = Router()


# Обработка получения статистики
@router.callback_query(F.data == "statistic_partner")
async def ask_buttons(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=await get_statistics_partners(),
        reply_markup=back_menu
    )
    await callback.answer()


# Обработка кнопки "Назад"
@router.callback_query(F.data == "go_back_menu")
async def back_buttons(callback: types.CallbackQuery):

    tg_id = callback.from_user.id
    await callback.message.edit_text(
        text=starting_parner_message,
        reply_markup=await get_partner_menu(tg_id)
    )
    await callback.answer()