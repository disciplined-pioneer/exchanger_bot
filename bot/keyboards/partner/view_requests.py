from settings import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Добавляем все заявки как кнопки для каждого из партнёров
async def get_partner_exchanges_keyboard(partner_id: int, page: int = 1, per_page: int = 5) -> InlineKeyboardMarkup:

    from db.models.models import Exchanges

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Поиск заявок не с 'COMPLETED' + id партнёра
    all_exchanges = await Exchanges.exclude(state='COMPLETED')
    all_exchanges_partner = [exchange for exchange in all_exchanges if exchange.partner_id == partner_id]
    
    # Рассчитываем нужный срез для пагинации
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    exchanges_page = all_exchanges_partner[start_index:end_index]
    
    # Добавляем кнопки для заявок на текущей странице
    for exchanges_partner in exchanges_page:
        amout_to = exchanges_partner.amout_to
        to_currency = exchanges_partner.to_currency
        platform = exchanges_partner.platform
        client_id = exchanges_partner.client_id

        # Добавляем кнопку
        button = InlineKeyboardButton(
            text=f'{amout_to} {to_currency} {platform} | {client_id}',
            callback_data=f'exchange:{exchanges_partner.id}'
        )
        keyboard.inline_keyboard.append([button])
    
    # Добавляем кнопки для навигации по страницам, если есть еще страницы
    navigation_buttons = []
    if page > 1:
        prev_page_button = InlineKeyboardButton(
            text="⬅️ Назад", callback_data=f"exchanges_prev:{page - 1}"
        )
        navigation_buttons.append(prev_page_button)

    if len(all_exchanges_partner) > end_index:
        next_page_button = InlineKeyboardButton(
            text="➡️ Вперёд", callback_data=f"exchanges_next:{page + 1}"
        )
        navigation_buttons.append(next_page_button)

    if navigation_buttons:
        keyboard.inline_keyboard.append(navigation_buttons)  # Добавляем их в одну строку
    
    # Кнопка назад в меню
    keyboard.inline_keyboard.append([InlineKeyboardButton(text='🔙 Меню', callback_data='go_back_menu')])

    return keyboard


back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Меню", callback_data="go_back_menu")]
    ]
)