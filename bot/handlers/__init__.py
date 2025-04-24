from bot.handlers.user.start import router as start
from bot.handlers.admin.statistics import router as statistics

routers = [
    start,
    statistics
]
