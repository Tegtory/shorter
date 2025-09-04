import logging

from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka

from shorter.infrastructure.di import container
from shorter.presentors.aiogram.handlers import router

logger = logging.getLogger(__name__)


async def main(token: str | None = None) -> None:
    if not token:
        logger.warning("BOT TOKEN MISSING")
        return
    logger.info("Starting aiogram bot")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    setup_dishka(container, dp)
    logger.info("Bot started")
    await dp.start_polling(bot, skip_updates=True)
