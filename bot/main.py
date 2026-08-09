import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.auth import GlobalAdminAuthMiddleware
from bot.handlers import common, portfolio, services, about, contacts, settings, orders, videos, stats, admins

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables.")
        return

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Attach Global Admin Auth Middleware (Enforces Private Admin Access)
    dp.message.middleware(GlobalAdminAuthMiddleware())
    dp.callback_query.middleware(GlobalAdminAuthMiddleware())

    # Include Admin Routers
    dp.include_router(common.router)
    dp.include_router(portfolio.router)
    dp.include_router(services.router)
    dp.include_router(about.router)
    dp.include_router(contacts.router)
    dp.include_router(settings.router)
    dp.include_router(orders.router)
    dp.include_router(videos.router)
    dp.include_router(stats.router)
    dp.include_router(admins.router)

    logger.info("🤖 Private Aiogram 3 Telegram Admin Bot control center started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
