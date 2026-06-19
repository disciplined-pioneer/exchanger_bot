from bot.handlers.user.start import router as start
from bot.handlers.admin.ban import router as ban
from bot.handlers.admin.broadcast import router as broadcast
from bot.handlers.admin.statistics import router as statistics
from bot.handlers.admin.add_partner import router as add_partner
from bot.handlers.admin.commissions import router as commissions
from bot.handlers.admin.delete_exchange import router as delete_exchange

from bot.handlers.user.clear_state import router as clear_state
from bot.handlers.user.exchange_currency import router as exchange_currency
from bot.handlers.user.user_details import router as user_details
from bot.handlers.user.exchange_confirmation import router as exchange_confirmation

from bot.handlers.partner.reply_to_user import router as reply_to_user
from bot.handlers.partner.view_requests import router as view_requests
from bot.handlers.partner.my_offers import router as my_offers
from bot.handlers.partner.create_offer import router as create_offer
from bot.handlers.partner.statistics import router as statistics_part
from bot.handlers.partner.result_exchange import router as result_exchange
from bot.handlers.partner.send_details import router as receiving_application
from bot.handlers.partner.work_status import router as work_status


routers = [
    start,
    ban,
    broadcast,
    statistics,
    add_partner,
    delete_exchange,
    commissions,
    work_status,
    
    exchange_currency,
    user_details,
    exchange_confirmation,

    reply_to_user,
    view_requests,
    my_offers,
    create_offer,
    statistics_part,
    result_exchange,
    receiving_application,
    clear_state
]
