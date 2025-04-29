from aiogram import Router, F, types
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext

from core.bot import bot
from utils.user.user_details import *


router = Router()


# Обработчик кнопки "Я оплатил" у партнёра
@router.callback_query(F.data == "user_paid")
async def user_paid(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    tg_id = int(data.get('tg_id', ''))

    # Сообщение партнёру
    await callback.message.delete()
    await callback.message.answer('✅ Вы подтвердили оплату! Сообщение отправлено пользователю!')

    # Отправляем сообщение пользователю
    await bot.send_message(
        chat_id=tg_id,
        text='Партнёр подтвердил оплату, завершите сделку, если не завершите в течении 24 часов - сделка завершится автоматически',
        reply_markup=None # ТУТ КНОПКА ДОЛЖНА БЫТЬ
    )

    
# Обработчик кнопки "Деньгине пришли" у партнёра
@router.callback_query(F.data == "user_not_paid")
async def user_not_paid(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    tg_id = int(data.get('tg_id', ''))
    
    # Сообщение партнёру
    await callback.message.delete()
    await callback.message.answer('✅ Сообщение отправлено пользователю!')

    # Отправляем сообщение пользователю
    state_message = await bot.send_message(
        chat_id=tg_id,
        text='Партнёр не получил оплату, пожалуйста, загрузите чек ещё раз. А также проверьте правильность написания реквизитов: номер карты, банк, ФИО'
    )

    # Устанавливаем состояние для пользователя по его id
    user_state = FSMContext(
        storage=state.storage,
        key=StorageKey(bot_id=state.key.bot_id, chat_id=tg_id, user_id=tg_id)
    )
    await user_state.set_state(PaymentState.user_details)
    await user_state.update_data({"last_id_message": state_message.message_id})