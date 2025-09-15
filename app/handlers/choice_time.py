from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from infrastructure.database.models import Services
from keyboards import kb
from states.order import Order
import datetime as dt

router = Router(name=__name__)


@router.callback_query(F.data == "back_from_booking", Order.approved)
@router.callback_query(F.data.startswith("choice_date_"), Order.day)
async def choice_date_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("choice_date_"):
        date_str = callback.data.split("_")[-1]
        selected_date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
    elif callback.data == "back_from_booking":
        selected_date = await state.get_value("selected_date")

    selected_services = await state.get_value("selected_services")

    await state.update_data({"selected_date": selected_date})

    await state.set_state(Order.time)

    text = (
        "Запись на "
        + selected_date.strftime("%d.%m.%Y")
        + " на услугу(и): "
        + ", ".join([s.name for s in selected_services if s is not None])
        + "\nВыберите время:"
    )

    await callback.message.answer(
        text, reply_markup=await kb.time_keyboard(selected_date, selected_services)
    )

    await callback.message.delete()


@router.callback_query(F.data.startswith("book_"), Order.time)
async def book_time_handler(callback: CallbackQuery, state: FSMContext):
    _, date_str, start_time, end_time = callback.data.split("_")
    date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()

    await state.update_data({"start_time": start_time, "end_time": end_time})

    await state.set_state(Order.approved)

    selected_services: list[Services] = await state.get_value("selected_services")

    sum_duration_minutes = sum(s.duration_minutes for s in selected_services)

    sum_price = sum(s.price for s in selected_services)

    text = (
        f"Подтвердите запись на {date.strftime('%d.%m.%Y')} с {start_time} до {end_time} на услугу(и): "
        + ", ".join([s.name for s in selected_services])
        + f".\nОбщая длительность: {sum_duration_minutes // 60} ч {sum_duration_minutes % 60} мин"
        + f".\nОбщая стоимость: {sum_price} руб."
        + ".\nАдрес: г. Уфа, ул. Маршала Жукова, дом 15, квартира 1"
        + "\n\nНомер мастера: 8 800 555 35 35"
    )

    await callback.message.answer(text, reply_markup=kb.booking_keyboard())

    await callback.message.delete()
