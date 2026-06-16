import logging
import asyncio
from aiogram import Dispatcher
from aiogram.types import BotCommandScopeDefault

from core.bot import bot
from bot.handlers import routers

from settings import settings
from db.crud.base import init_postgres
from services.report_timer import reporter_loop
from services.init_users import register_initial_users


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

dp = Dispatcher()
dp.include_routers(*routers)


async def main():

    await init_postgres()
    await register_initial_users() # Добавляем админов и партнёров

    print("АДМИНЫ:", settings.bot.ADMINS)

    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text='✅ Бот запущен'
    )

    #asyncio.create_task(reporter_loop()) # Фоновая задача
    
    await bot.set_my_commands(
        commands=settings.bot.COMMANDS,
        scope=BotCommandScopeDefault()
    )
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    
    try:
        print("\n✅ Бот запущен\n")
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен 🛑\n")

    except Exception as e:
        print(f"\n❌ Возникла ошибка : {e}\n")