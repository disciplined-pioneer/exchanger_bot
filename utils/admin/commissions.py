from aiogram.fsm.state import StatesGroup, State


class RequestCommissions(StatesGroup):
    request = State()