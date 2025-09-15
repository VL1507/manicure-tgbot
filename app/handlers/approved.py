import datetime as dt

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from infrastructure.database.requests import save_appointments
from keyboards import kb
from states.order import Order

router = Router(name=__name__)


@router.callback_query(F.data == "approved", Order.approved)
async def approve_booking(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    date: dt.date = await state.get_value("selected_date")
    time_start: str = await state.get_value("start_time")
    time_end: str = await state.get_value("end_time")

    selected_services_id: list[int] = await state.get_value("selected_services_id")

    await save_appointments(
        user_id=user_id,
        date=date,
        time_start=time_start,
        time_end=time_end,
        selected_services_id=selected_services_id,
    )

    await callback.answer("Успешно")
    await state.clear()

    await callback.message.answer(
        "Привет! Это бот для записи к мастеру салона красоты 'Мадина'!",
        reply_markup=kb.start,
    )
    await callback.message.delete()
