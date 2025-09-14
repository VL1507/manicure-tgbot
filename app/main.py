import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings

from handlers import router as main_router


async def main():
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    dp.include_router(main_router)

    bot = Bot(
        token=settings.BOT.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
