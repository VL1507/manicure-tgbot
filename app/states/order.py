from aiogram.fsm.state import State, StatesGroup


class Order(StatesGroup):
    service = State()

    day = State()
    time = State()
    approved = State()
