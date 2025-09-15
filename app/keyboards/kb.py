import datetime as dt

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from infrastructure.database.models import Services
from infrastructure.database.requests import get_available_slots

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
        [InlineKeyboardButton(text="Готово", callback_data="next_from_service")]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def days_keyboard(offset_days: int, work_duration: int):
    inline_keyboard = []

    target_date = dt.datetime.now().date() + dt.timedelta(days=offset_days)

    dates = []
    available_dates = []

    for i in range(7):
        current_date = target_date + dt.timedelta(days=i)

        if current_date > dt.datetime.now().date() + dt.timedelta(days=365):
            continue

        dates.append(current_date)

        available_slots = await get_available_slots(current_date, work_duration)
        if len(available_slots) > 0:
            available_dates.append(current_date)

    # print(available_dates)

    date_buttons = []
    for date_ in dates:
        if date_ in available_dates:
            date_buttons.append(
                [
                    InlineKeyboardButton(
                        text=date_.strftime("%d.%m.%Y"),
                        callback_data=f"choice_date_{date_.strftime('%Y-%m-%d')}",
                    )
                ]
            )
        else:
            date_buttons.append(
                [
                    InlineKeyboardButton(
                        text=date_.strftime("%d.%m.%Y") + " ❌",
                        callback_data="no_slots",
                    )
                ]
            )
    navigation_buttons = []

    if offset_days > 0:
        new_offset = max(0, offset_days - 7)
        navigation_buttons.append(
            InlineKeyboardButton(
                text="◀️◀️", callback_data=f"date_navigation_{new_offset}"
            )
        )

    if offset_days < 358:
        new_offset = min(offset_days + 7, 358)
        navigation_buttons.append(
            InlineKeyboardButton(
                text="▶️▶️", callback_data=f"date_navigation_{new_offset}"
            )
        )

    inline_keyboard.extend(date_buttons)
    inline_keyboard.append(navigation_buttons)

    inline_keyboard.append(
        [InlineKeyboardButton(text="Назад", callback_data="back_from_date")]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def time_keyboard(
    date_: dt.date, selected_services: list[Services]
) -> InlineKeyboardMarkup:
    inline_keyboard = []

    available_slots = await get_available_slots(
        date_, sum([s.duration_minutes for s in selected_services])
    )

    if available_slots:
        for slot in available_slots:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=slot[0] + " - " + slot[1],
                        callback_data=f"book_{date_.strftime('%Y-%m-%d')}_{slot[0]}_{slot[1]}",
                    )
                ]
            )
    else:
        # по идее это не может произойти. оставил на случай, если где-то ошибся
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="Нет доступных слотов", callback_data="no_slots"
                )
            ]
        )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Назад", callback_data="back_from_time")]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def booking_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = []

    inline_keyboard.append(
        [InlineKeyboardButton(text="Подтвердить", callback_data="approved")]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Назад", callback_data="back_from_booking")]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
