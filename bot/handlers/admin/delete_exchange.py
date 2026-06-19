from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from utils.admin.commissions import *
from bot.keyboards.admin.delete_exchange import *

from core.bot import bot
from settings import settings
from db.models.models import Exchanges


router = Router()


# Обработка кнопки "Удалить обмен"
@router.callback_query(F.data == "delete_exchange")
async def delete_exchange(callback: types.CallbackQuery, state: FSMContext):
    
    await callback.answer()
    await callback.message.edit_text(
        text='Выберите обмен для удаления',
        reply_markup=await get_all_exchange_keyboard()
    )


# Обработка кнопки выбранного для удаления обмена
@router.callback_query(F.data.startswith("ex_del:"))
async def ex_del(callback: types.CallbackQuery, state: FSMContext):

    # Поиск и удаление обмена
    ex_id = int(callback.data.split(':')[1])
    ex_info = await Exchanges.get(id=ex_id)
    await ex_info.delete()
    await callback.message.edit_text(
        text=f'Обмен был удалён №{ex_id}'
    )