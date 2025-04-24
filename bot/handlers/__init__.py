from bot.handlers.user.start import router as start
from bot.handlers.admin.broadcast import router as broadcast
from bot.handlers.admin.statistics import router as statistics
from bot.handlers.partner.currency_rate_update import router as currency_rate_update

routers = [
    start,
    broadcast,
    statistics,
    currency_rate_update
]
