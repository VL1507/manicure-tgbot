__all__ = ("router",)

from aiogram import Router

from handlers import other_message

router = Router(name=__name__)

router.include_router(other_message.router)
