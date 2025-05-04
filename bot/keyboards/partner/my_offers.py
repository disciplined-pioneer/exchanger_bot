from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_menu_rate(context: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"go_back_rate:{context}")]
        ]
    )

back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Меню", callback_data=f"go_back_menu")]
    ]
)

async def build_rates_keyboard_for_partner(partner_id: int) -> InlineKeyboardMarkup:
    from db.models.models import Rates  # перемести внутрь, чтобы избежать циклического импорта

    keyboard = InlineKeyboardMarkup(inline_keyboard=[]) 
    all_rates_partner = await Rates.filter(partner_id=partner_id)

    for rate_partner in all_rates_partner:
        rate = rate_partner.rate
        limits = rate_partner.limits
        from_currency = rate_partner.from_currency
        to_currency = rate_partner.to_currency
        platform = rate_partner.platform

        button = InlineKeyboardButton(
            text=f'{rate} {from_currency} → {to_currency} ({platform}) | {limits}',
            callback_data=f'rate:{rate_partner.id}'
        )
        keyboard.inline_keyboard.append([button])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='🔙 Назад', callback_data='go_back_menu')
    ])

    return keyboard

async def actions_with_course(rate_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Редактировать курс", callback_data=f"edit_rate:{rate_id}")],
            [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_rate:{rate_id}")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"go_back_rate:rates_list")]
        ]
    )
