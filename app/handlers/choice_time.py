from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards import kb
from states.order import Order
import datetime as dt

router = Router(name=__name__)


@router.callback_query(F.data.startswith("choice_date_"), Order.day)
async def choice_date_handler(callback: CallbackQuery, state: FSMContext):
    date_str = callback.data.split("_")[-1]
    selected_date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()

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
