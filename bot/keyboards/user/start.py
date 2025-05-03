from settings import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.models.models import Exchanges

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
    
    exchanges = await Exchanges.get(partner_id=tg_id)
    count_exchanges = len(exchanges) if exchanges else 0

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Создать объявление", callback_data="create_offer")],
            [InlineKeyboardButton(text="📋 Мои объявления - СДЕЛАТЬ", callback_data="my_offers")],
            [InlineKeyboardButton(text=f"📥 Заявки ({count_exchanges}) - СДЕЛАТЬ", callback_data="view_requests")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="statistic_partner")]
        ]
    )

    return keyboard

start_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поддержка", url=settings.bot.SUPPORT_LINK)],
        [InlineKeyboardButton(text="Выбрать партнёра", callback_data="select_partner")]
    ]
)