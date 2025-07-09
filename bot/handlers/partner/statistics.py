from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.user.start import *
from bot.templates.user.start import *

from bot.templates.partner.statistics import *
from bot.keyboards.partner.statistics import back_menu


router = Router()


# Обработка получения статистики
@router.callback_query(F.data == "statistic_partner")
async def ask_buttons(callback: types.CallbackQuery):

    await callback.answer()

    # Убираем кнопки из старого сообщения, не меняя текст
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # Отправляем новое сообщение с текстом статистики и кнопкой "Назад"
    await callback.message.answer(
        text=await get_statistics_partners(partner_id=callback.from_user.id),
        reply_markup=back_menu
    )
