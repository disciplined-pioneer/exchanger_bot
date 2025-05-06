from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.user.start import get_partner_menu
from bot.templates.user.start import starting_parner_message

from bot.templates.partner.statistics import *
from bot.keyboards.user.start import *
from bot.templates.user.start import *
from bot.keyboards.partner.statistics import back_menu

from db.models.models import Users


router = Router()


# Обработка получения статистики
@router.callback_query(F.data == "statistic_partner")
async def ask_buttons(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=await get_statistics_partners(),
        reply_markup=back_menu
    )
    await callback.answer()
