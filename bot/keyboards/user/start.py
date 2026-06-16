from settings import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.models.models import Exchanges, Partners, Rates

start_admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💰 Запросить комиссии", callback_data="request_commissions")],
        [InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="➕ Добавить партнёра", callback_data="add_partner")],
        [InlineKeyboardButton(text="🚫 Бан", callback_data="ban_user")]
    ]
)

back_admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="start_menu_admin")]
    ]
)

update_rate_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить курс", callback_data="update_rate_partner")]
    ]
)


async def get_partner_menu(tg_id: int):
    
    # Заявки
    partner_info = await Partners.get(tg_id=tg_id)
    all_exchanges = await Exchanges.exclude(state=['COMPLETED', 'CANCELLED'])
    count_exchanges = len([exchange for exchange in all_exchanges if exchange.partner_id == partner_info.id])

    # Объявления
    info_partner_rates = await Rates.filter(partner_id=partner_info.id)
    count = len(info_partner_rates)

    # Статус партнёра
    info_partner = await Partners.get(tg_id=tg_id)
    is_active = info_partner.status  # True / False

    status_text = "🟢 Я работаю" if is_active else "🔴 Я не работаю"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Создать объявление", callback_data="create_offer")],
            [InlineKeyboardButton(text=f"📋 Мои объявления ({count})", callback_data="my_offers")],
            [InlineKeyboardButton(text=f"📥 Заявки ({count_exchanges})", callback_data="view_requests")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="statistic_partner")],
            [InlineKeyboardButton(text=status_text, callback_data="toggle_status")]  # кнопка смены статуса
        ]
    )

    return keyboard


start_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поддержка", url=settings.bot.SUPPORT_LINK)],
        [InlineKeyboardButton(text="Обменять валюту", callback_data="exchange_currency")]
    ]
)