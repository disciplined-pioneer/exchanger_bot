from settings import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💰 Запросить комиссии - ДОРАБОТАТЬ", callback_data="request_commissions")],
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


start_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поддержка", url=settings.bot.SUPPORT_LINK)],
        [InlineKeyboardButton(text="Выбрать партнёра", callback_data="select_partner")]
    ]
)