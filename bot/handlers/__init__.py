from bot.handlers.user.start import router as start
from bot.handlers.user.topic import router as topic
from bot.handlers.admn.broadcast import router as broadcast

routers = [
    start,
    broadcast,
    topic
]
