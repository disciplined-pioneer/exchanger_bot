from bot.handlers.user.start import router as start
from bot.handlers.admin.broadcast import router as broadcast
from bot.handlers.admin.statistics import router as statistics

from bot.handlers.user.user_details import router as user_details
from bot.handlers.user.request_details import router as request_details
from bot.handlers.user.exchange_confirmation import router as exchange_confirmation

from bot.handlers.partner.result_exchange import router as result_exchange
from bot.handlers.partner.currency_rate_update import router as currency_rate_update
from bot.handlers.partner.receiving_application import router as receiving_application


routers = [
    start,
    broadcast,
    statistics,
    
    user_details,
    request_details,
    exchange_confirmation,

    result_exchange,
    currency_rate_update,
    receiving_application
]
