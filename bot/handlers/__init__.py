from bot.handlers.user.start import router as start
from bot.handlers.admin.broadcast import router as broadcast
from bot.handlers.admin.statistics import router as statistics
from bot.handlers.partner.currency_rate_update import router as currency_rate_update

from bot.handlers.user.request_details import router as request_details
from bot.handlers.partner.receiving_application import router as receiving_application

routers = [
    start,
    broadcast,
    statistics,
    currency_rate_update,
    request_details,
    receiving_application
]
