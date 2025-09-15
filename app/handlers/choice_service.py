from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from infrastructure.database.requests import get_services
from keyboards import kb
from states.order import Order

router = Router(name=__name__)


@router.callback_query(F.data == "order")
async def order_callback_handler(callback: CallbackQuery, state: FSMContext):
    all_services = await get_services()

    await callback.message.answer(
        "Выберите желаемую услугу:", reply_markup=kb.service_keyboard(all_services)
    )

    await state.set_state(Order.service)

    selected_services_id = []
    await state.update_data({"selected_services_id": selected_services_id})


@router.callback_query(F.data.startswith("service_"), Order.service)
async def service_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.service)

    service_id = int(callback.data.split("_")[1])

    selected_services_id: list[int] = await state.get_value("selected_services_id")

    selected_services_id.append(service_id)

    await state.update_data({"selected_services_id": selected_services_id})

    all_services = await get_services()
    not_selected_services = [
        s for s in all_services if s.id not in selected_services_id
    ]

    text = (
        "Выбрана(ы) услуга(и):\n"
        + "\n".join([s.name for s in all_services if s.id in selected_services_id])
        + "\n\nЖелаете дополнительные услуги?"
    )
    try:
        await callback.message.edit_text(
            text, reply_markup=kb.service_keyboard(not_selected_services)
        )
    except Exception:
        await callback.message.answer(
            text, reply_markup=kb.service_keyboard(not_selected_services)
        )
