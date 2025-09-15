__all__ = ("router",)

from aiogram import Router

from handlers import (
    approved,
    back_from_date,
    cancel,
    choice_day,
    choice_service,
    choice_time,
    other_message,
    start,
)

router = Router(name=__name__)

router.include_routers(
    choice_service.router,
    cancel.router,
    start.router,
    choice_day.router,
    back_from_date.router,
    choice_time.router,
    approved.router,
)


# должен быть последним
router.include_router(other_message.router)
