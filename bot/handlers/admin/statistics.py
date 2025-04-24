from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from bot.keyboards.user.start import back_admin_keyb
from bot.templates.admin.statistics import get_monthly_exchange_report


router = Router()


# Обработка получения статистики
@router.callback_query(F.data == "admin_stats")
async def ask_buttons(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        await get_monthly_exchange_report(),
        reply_markup=back_admin_keyb
    )
    await callback.answer()