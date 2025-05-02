from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from utils.admin.commissions import *
from bot.keyboards.admin.commissions import *
from bot.templates.admin.commissions import *

from datetime import datetime
from db.models.models import Commissions

from core.bot import bot
from settings import settings


router = Router()


# Обработка "Запросить комиссии"
@router.callback_query(F.data == "request_commissions")
async def start_commissions(callback: types.CallbackQuery, state: FSMContext):
    
    await callback.message.edit_text(
        text=await commission_info_message(),
        reply_markup=request_partner_keyboard
    )
    await state.set_state(RequestCommissions.request)


# Обработка кнопки "Запросить"
@router.callback_query(F.data == "request")
async def request_commissions(callback: types.CallbackQuery, state: FSMContext):

    # Отправляем сообщения партнёрам
    info_partners = await Partners.all()
    for user in info_partners:
        try:
            # Отправляем сообщение партнёру
            await bot.send_message(
                chat_id=user.tg_id,
                text=commission_payment_message(),
                reply_markup=paid_commission_keyb
            )
            
            # Активируем ему состояние
            partner_state = FSMContext(
                storage=state.storage,
                key=state.key.__class__(bot_id=state.key.bot_id, chat_id=user.tg_id, user_id=user.tg_id)
            )
            await partner_state.set_state(RequestCommissions.request)

        except Exception as e:
            continue  # Переходим к следующему

    await callback.message.edit_text(messages_sent_message)
    await state.clear()


# Обработка кнопки "Я оплатил"
@router.callback_query(F.data == "paid_commission")
async def request_commissions(callback: types.CallbackQuery, state: FSMContext):

    # Добавляем комиссию в БД
    now = datetime.now()
    await Commissions.create(
        date=now,
        commissions=settings.bot.COMMISSION
    )

    await callback.message.edit_text(
        text=payment_confirmed_message
    )

    # Отправляем сообщение админу
    for tg_id in settings.bot.ADMINS:
        try:
            await bot.send_message(
                chat_id=tg_id,
                text=await partner_paid_commission_message(tg_id)
            )
        except Exception as e:
            print(f"Не удалось отправить админу {tg_id}: {e}")
            continue

    await state.clear()


# Удаление сообщения при RequestCommissions.request
@router.message(RequestCommissions.request)
async def request_commissions_mess(message: types.Message, state: FSMContext):
    await message.delete()