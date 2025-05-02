from aiogram.fsm.state import StatesGroup, State


class AddPartner(StatesGroup):
    current_index = State()
    values = State()


PARTNER_QUESTIONS = {
    "telegram_id": "Введите Telegram ID партнёра",
    "name": "Введите имя партнёра"
}
