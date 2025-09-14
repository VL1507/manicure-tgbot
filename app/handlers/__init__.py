__all__ = ("router",)

from aiogram import Router

from handlers import order, other_message, cancel, start

router = Router(name=__name__)

router.include_routers(order.router, cancel.router, start.router)


# должен быть последним
router.include_router(other_message.router)
