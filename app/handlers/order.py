from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from infrastructure.database.requests import get_services
from keyboards import kb


router = Router(name=__name__)


class Order(StatesGroup):
    service = State()

    day = State()
    time = State()
    approved = State()


@router.callback_query(F.data == "order")
async def order_callback_handler(callback: CallbackQuery, state: FSMContext):
    all_services = await get_services()

    await callback.message.answer(
        "Выберите желаемую услугу:", reply_markup=kb.service_keyboard(all_services)
    )

    await state.set_state(Order.service)

    selected_services = []
    await state.update_data({"selected_services": selected_services})


@router.callback_query(F.data.startswith("service_"), Order.service)
async def service_callback_handler(callback: CallbackQuery, state: FSMContext):
    service_id = int(callback.data.split("_")[1])

    selected_services: list[int] = await state.get_value("selected_services")

    selected_services.append(service_id)

    await state.update_data({"selected_services": selected_services})

    all_services = await get_services()
    not_selected_services = [s for s in all_services if s.id not in selected_services]

    text = (
        "Выбрана(ы) услуга(и):\n"
        + "\n".join([s.name for s in all_services if s.id in selected_services])
        + "\n\nЖелаете дополнительные услуги?"
    )
    await callback.message.answer(
        text, reply_markup=kb.service_keyboard(not_selected_services)
    )
