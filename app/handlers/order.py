from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from infrastructure.database.requests import get_services, get_service_by_id
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

    selected_services_id = []
    await state.update_data({"selected_services_id": selected_services_id})


@router.callback_query(F.data.startswith("service_"), Order.service)
async def service_callback_handler(callback: CallbackQuery, state: FSMContext):
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
    except Exception as e:
        await callback.message.answer(
            text, reply_markup=kb.service_keyboard(not_selected_services)
        )


@router.callback_query(F.data == "next_from_service", Order.service)
async def next_from_service_handler(callback: CallbackQuery, state: FSMContext):
    selected_services_id: list[int] = await state.get_value("selected_services_id")

    if len(selected_services_id) == 0:
        await callback.answer("Необходимо выбрать услугу(и)", show_alert=True)
        return

    await state.set_state(Order.day)

    selected_services = [await get_service_by_id(sid) for sid in selected_services_id]

    await state.update_data({"selected_services": selected_services})

    text = (
        "На какой день запишемся на услугу(и): "
        + ", ".join([s.name for s in selected_services if s is not None])
        + "?"
    )

    work_duration = sum([s.duration_minutes for s in selected_services])

    await callback.message.answer(
        text,
        reply_markup=await kb.days_keyboard(offset_days=0, work_duration=work_duration),
    )
    await callback.message.delete()
