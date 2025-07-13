import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers.admin_handlers import admin_router
from bot.handlers.user_handlers import user_router
from config import BOT_TOKEN



async def startup():
    print('Bot is starting...')

async def shutdown():
    print('Bot is shutting down...')

async def main():
    bot = Bot(token = BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(user_router, admin_router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass