from bot.handlers.user.start import router as start
from bot.handlers.admin.broadcast import router as broadcast
from bot.handlers.admin.statistics import router as statistics

routers = [
    start,
    broadcast,
    statistics
]
