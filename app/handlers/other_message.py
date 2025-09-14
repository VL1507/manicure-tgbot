from aiogram import Router
from aiogram.types import Message


router = Router(name=__name__)


@router.message()
async def other_message(message: Message):
    await message.answer("Команда не распознана. Ведите /start")
