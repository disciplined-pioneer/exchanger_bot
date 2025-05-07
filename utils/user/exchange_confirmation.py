from aiogram.fsm.state import State, StatesGroup

class MessagingStates(StatesGroup):
    user_message = State()
    partner_message = State()