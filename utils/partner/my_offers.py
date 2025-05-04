import re
from datetime import datetime
from db.models.models import Rates
from aiogram.fsm.state import StatesGroup, State

class RateEdit(StatesGroup):
    rate = State()