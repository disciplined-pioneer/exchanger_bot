from bot.handlers.user.start import router as start
from bot.handlers.admin.ban import router as ban
from bot.handlers.admin.broadcast import router as broadcast
from bot.handlers.admin.statistics import router as statistics
from bot.handlers.admin.add_partner import router as add_partner
from bot.handlers.admin.commissions import router as commissions

from bot.handlers.user.user_details import router as user_details
from bot.handlers.user.request_details import router as request_details
from bot.handlers.user.exchange_confirmation import router as exchange_confirmation

from bot.handlers.partner.create_offer import router as create_offer
from bot.handlers.partner.statistics import router as statistics_part
from bot.handlers.partner.result_exchange import router as result_exchange
from bot.handlers.partner.currency_rate_update import router as currency_rate_update
from bot.handlers.partner.receiving_application import router as receiving_application


routers = [
    start,
    ban,
    broadcast,
    statistics,
    add_partner,
    commissions,
    
    user_details,
    request_details,
    exchange_confirmation,

    create_offer,
    statistics_part,
    result_exchange,
    currency_rate_update,
    receiving_application
]
