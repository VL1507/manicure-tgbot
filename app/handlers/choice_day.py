from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from infrastructure.database.requests import get_service_by_id
from keyboards import kb
from states.order import Order

router = Router(name=__name__)


@router.callback_query(F.data == "back_from_time", Order.time)
@router.callback_query(F.data.startswith("date_navigation_"), Order.day)
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

    offset_days = 0
    if callback.data.startswith("date_navigation_"):
        offset_days = int(callback.data.split("_")[-1])

    await callback.message.answer(
        text,
        reply_markup=await kb.days_keyboard(
            offset_days=offset_days, work_duration=work_duration
        ),
    )
    await callback.message.delete()


@router.callback_query(F.data == "no_slots", Order.day)
async def no_slots_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer(
        "К сожалению, на выбранную дату нет доступных мест.", show_alert=True
    )
