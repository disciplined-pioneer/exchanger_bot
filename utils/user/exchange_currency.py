from aiogram.fsm.state import State, StatesGroup

class ExchangeStates(StatesGroup):
    sum = State()
    plug = State()
    details = State()
    partner_details = State()