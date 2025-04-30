from aiogram.fsm.state import State, StatesGroup

class ExchangeStates(StatesGroup):
    summ = State()
    details = State()
    partner_details = State()