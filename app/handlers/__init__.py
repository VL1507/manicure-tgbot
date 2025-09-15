__all__ = ("router",)

from aiogram import Router

from handlers import (
    other_message,
    cancel,
    start,
    choice_day,
    back_from_date,
    choice_service,
)

router = Router(name=__name__)

router.include_routers(
    choice_service.router,
    cancel.router,
    start.router,
    choice_day.router,
    back_from_date.router,
)


# должен быть последним
router.include_router(other_message.router)
