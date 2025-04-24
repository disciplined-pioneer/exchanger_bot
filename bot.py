import logging
import asyncio
from aiogram import Dispatcher
from aiogram.types import BotCommandScopeDefault

from core.bot import bot
from bot.handlers import routers

from settings import settings
from db.crud.base import init_postgres


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
dp.include_routers(*routers)


async def main():
    await init_postgres()
    await bot.set_my_commands(
        commands=settings.bot.COMMANDS,
        scope=BotCommandScopeDefault()
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    
    try:
        print("\nБот запущен ✅\n")
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен 🛑\n")

    except Exception as e:
        print(f"\n❌ Возникла ошибка : {e}\n")