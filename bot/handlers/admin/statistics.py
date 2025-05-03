from aiogram import Router, F, types
from bot.templates.user.start import starting_admin_message
from bot.keyboards.user.start import back_admin_keyb, start_admin_keyb
from bot.templates.admin.statistics import get_monthly_exchange_report


router = Router()


# Обработка получения статистики
@router.callback_query(F.data == "admin_stats")
async def ask_buttons(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=await get_monthly_exchange_report(),
        reply_markup=back_admin_keyb
    )
    await callback.answer()


# Обработка кнопки "Назад"
@router.callback_query(F.data == "start_menu_admin")
async def back_buttons(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=starting_admin_message,
        reply_markup=start_admin_keyb
    )
    await callback.answer()