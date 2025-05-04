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
    exchanges = await Exchanges.filter(partner_id=tg_id)
    count_exchanges = len(exchanges) if exchanges else 0

    # Объявления (смотрим количество существующих значений в БД)
    count = 0
    info_partner = await Partners.get(tg_id=tg_id)
    active_pairs = info_partner.active_pairs
    for info in active_pairs:
        result = await Rates.get_latest_rate(
            partner_id=tg_id,
            from_currency=info.get('from', ''),
            to_currency=info.get('to', ''),
            platform=info.get('platform', '')
        )

        if result is not None:
            count += 1

    # Возвращаем меню
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Создать объявление", callback_data="create_offer")],
            [InlineKeyboardButton(text=f"📋 Мои объявления ({count})", callback_data="my_offers")],
            [InlineKeyboardButton(text=f"📥 Заявки ({count_exchanges})", callback_data="view_requests")],
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