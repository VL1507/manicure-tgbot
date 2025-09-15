from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards import kb

router = Router(name=__name__)


@router.callback_query(F.data == "cancel")
async def cancel_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    # await callback.message.answer("Запись отменена.", reply_markup=kb.start)
    await callback.message.answer(
        "Привет! Это бот для записи к мастеру салона красоты 'Мадина'!",
        reply_markup=kb.start,
    )
    await callback.message.delete()
