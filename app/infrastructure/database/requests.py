import datetime as dt

from constants import SLOT_DURATION, WORK_TIME_END, WORK_TIME_START
from sqlalchemy import select

from infrastructure.database.accessor import get_db_session
from infrastructure.database.models import Appointments, Services, ServiceToAppointments


async def get_services() -> list[Services]:
    async with get_db_session() as session:
        stmt = select(Services)
        services = await session.execute(stmt)
        return list(services.scalars().all())


async def get_service_by_id(service_id: int) -> Services | None:
    async with get_db_session() as session:
        stmt = select(Services).where(Services.id == service_id)
        service = await session.execute(stmt)
        return service.scalar()


async def get_available_slots(
    date: dt.date, work_duration: int
) -> list[tuple[str, str]]:
    async with get_db_session() as session:
        stmt = select(Appointments).where(Appointments.date == date)
        result = await session.execute(stmt)
        appointments = list(result.scalars().all())

        booked_intervals = []
        for appointment in appointments:
            start_time = dt.datetime.strptime(appointment.time_start, "%H:%M").time()
            end_time = dt.datetime.strptime(appointment.time_end, "%H:%M").time()

            start_time_minutes = start_time.hour * 60 + start_time.minute
            end_time_minutes = end_time.hour * 60 + end_time.minute

            booked_intervals.append((start_time_minutes, end_time_minutes))

        available_slots: list[tuple[str, str]] = []

        if date != dt.datetime.now().date():
            work_start_minutes = WORK_TIME_START * 60
        else:
            work_start_minutes = max(
                WORK_TIME_START * 60,
                dt.datetime.now().hour * 60 + dt.datetime.now().minute,
            )
            work_start_minutes = (
                work_start_minutes // SLOT_DURATION + 1
            ) * SLOT_DURATION

        work_end_minutes = WORK_TIME_END * 60

        for start_minutes in range(
            work_start_minutes, work_end_minutes - work_duration + 1, SLOT_DURATION
        ):
            end_minutes = start_minutes + work_duration

            if end_minutes > work_end_minutes:
                continue

            is_available = True
            for booked in booked_intervals:
                if not (end_minutes <= booked[0] or start_minutes >= booked[1]):
                    is_available = False
                    break

            if is_available:
                start_time = dt.time(start_minutes // 60, start_minutes % 60)
                end_time = dt.time(end_minutes // 60, end_minutes % 60)
                available_slots.append(
                    (start_time.strftime("%H:%M"), end_time.strftime("%H:%M"))
                )

        return available_slots


async def save_appointments(
    user_id: int,
    date: dt.date,
    time_start: str,
    time_end: str,
    selected_services_id: list[int],
):
    async with get_db_session() as session:
        appointment = Appointments(
            user_id=user_id, date=date, time_start=time_start, time_end=time_end
        )

        session.add(appointment)

        await session.commit()
        await session.refresh(appointment)

        for service_id in selected_services_id:
            service_to_appointment = ServiceToAppointments(
                service_id=service_id, appointment_id=appointment.id
            )
            session.add(service_to_appointment)
        await session.commit()
