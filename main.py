import os
import asyncio

from dotenv import find_dotenv, load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from telegram.handlers import commands, new_order


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


async def main():
    dp = Dispatcher()
    dp.include_routers(commands.router_commands, new_order.router_new_order)

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )

    await Bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
