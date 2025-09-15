__all__ = ("router",)

from aiogram import Router

from handlers import order, other_message, cancel, start, choice_day

router = Router(name=__name__)

router.include_routers(order.router, cancel.router, start.router, choice_day.router)


# должен быть последним
router.include_router(other_message.router)
