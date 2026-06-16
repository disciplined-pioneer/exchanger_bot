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
    
    await callback.answer()
    await callback.message.edit_text(
        text=await commission_info_message(),
        reply_markup=request_partner_keyboard
    )
    await state.set_state(RequestCommissions.request)


# Обработка кнопки "Запросить"
@router.callback_query(F.data == "request")
async def request_commissions(callback: types.CallbackQuery, state: FSMContext):

    # Отправляем сообщения партнёрам
    await callback.answer()
    info_partners = await Partners.all()
    for partner in info_partners:
        try:
            # Отправляем сообщение партнёру
            commissions = await Exchanges.get_partner_commission(partner.id)
            if commissions != 0:
                await bot.send_message(
                    chat_id=partner.tg_id,
                    text=await commission_payment_message(commissions),
                    reply_markup=paid_commission_keyb(commissions)
                )
                
                # Активируем ему состояние
                partner_state = FSMContext(bot=bot, storage=state.storage, chat=partner.tg_id, user=partner.tg_id)
                await partner_state.update_data(commissions=commissions)
                await partner_state.set_state(RequestCommissions.request)

        except Exception as e:
            continue  # Переходим к следующему

    await callback.message.edit_text(
        text=messages_sent_message,
        reply_markup=back_menu
    )

    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text='📊 Администратор запросил статистику за месяц'
    )
    await state.clear()


# Обработка кнопки "Я оплатил"
@router.callback_query(F.data.startswith("paid_commission"))
async def request_commissions(callback: types.CallbackQuery, state: FSMContext):

    # Добавляем комиссию в БД
    await callback.answer()
    commissions = float(callback.data.split(':')[1])
    
    tg_id = callback.from_user.id
    partner = await Partners.get(tg_id=tg_id)
    await Commissions.create(
        partner_id=partner.id,
        commissions=commissions
    )

    await callback.message.edit_text(
        text=payment_confirmed_message
    )

    # Отправляем сообщение админу
    for tg_id in settings.bot.ADMINS:
        try:
            await bot.send_message(
                chat_id=tg_id,
                text=await partner_paid_commission_message(tg_id, partner.name, commissions)
            )
        except Exception as e:
            print(f"Не удалось отправить админу {tg_id}: {e}")
            continue

    await state.clear()


# Удаление сообщения при RequestCommissions.request
@router.message(RequestCommissions.request)
async def request_commissions_mess(message: types.Message, state: FSMContext):
    await message.delete()