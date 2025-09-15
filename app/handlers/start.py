from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import kb

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Привет! Это бот для записи к мастеру салона красоты 'Мадина'!",
        reply_markup=kb.start,
    )
