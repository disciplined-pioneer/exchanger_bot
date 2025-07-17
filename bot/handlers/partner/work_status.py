from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.user.start import get_partner_menu
from bot.templates.user.start import starting_parner_message

from db.models.models import Partners


router = Router()


# Изменение статуса работы
@router.callback_query(F.data == "toggle_status")
async def toggle_status(callback: types.CallbackQuery, state: FSMContext):

    tg_id = callback.from_user.id

    # Получаем партнёра и меняем статус
    info_partner = await Partners.get(tg_id=tg_id)
    new_status = not info_partner.status
    await info_partner.update(status=new_status)

    # Обновляем сообщение с новым статусом
    await callback.message.edit_text(
        text=starting_parner_message, 
        reply_markup=await get_partner_menu(tg_id)
    )