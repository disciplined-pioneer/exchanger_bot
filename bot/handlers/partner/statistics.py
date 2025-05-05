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


# Обработка кнопки "Назад"
@router.callback_query(F.data == "go_back_menu")
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):

    tg_id = callback.from_user.id
    info_users = await Users.get(tg_id=tg_id)
    role = info_users.role

    if role == 'admin': # Админ
        await callback.message.edit_text(
            text=starting_admin_message,
            reply_markup=start_admin_keyb
        )

    elif role == 'partner': # Парнёр
        await callback.message.edit_text(
            text=starting_parner_message,
            reply_markup=await get_partner_menu(tg_id)
        )

    else: # Пользователь
        await callback.message.edit_text(
            text=starting_user_message,
            reply_markup=start_user_keyb
        )

    await state.clear()
    await callback.answer()