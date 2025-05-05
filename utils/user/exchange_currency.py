from aiogram.fsm.state import State, StatesGroup

class ExchangeStates(StatesGroup):
    summ = State()
    plug = State()
    details = State()
    partner_details = State()

    summ2 = State()