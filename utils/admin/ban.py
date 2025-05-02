from aiogram.fsm.state import StatesGroup, State


class UserBan(StatesGroup):
    tg_id = State()