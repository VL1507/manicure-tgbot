from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from infrastructure.database.models import Services


start = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Записаться", callback_data="order")]]
)


def service_keyboard(services: list[Services]) -> InlineKeyboardMarkup:
    inline_keyboard = []

    i = 0
    len_services = len(services)

    while i < len_services:
        service = services[i]
        kb_service = [
            InlineKeyboardButton(
                text=service.name, callback_data=f"service_{service.id}"
            )
        ]
        i += 1
        if len_services - i > 0:
            service = services[i]
            kb_service.append(
                InlineKeyboardButton(
                    text=service.name, callback_data=f"service_{service.id}"
                )
            )
            i += 1

        inline_keyboard.append(kb_service)

    inline_keyboard.append(
        [InlineKeyboardButton(text="Готово", callback_data="next_service")]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
