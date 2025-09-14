from sqlalchemy import select

from infrastructure.database.accessor import get_db_session
from infrastructure.database.models import Appointments, Services, ServiceToAppointments


async def get_services():
    async with get_db_session() as session:
        stmt = select(Services)
        services = await session.execute(stmt)
        return list(services.scalars().all())
