from aiogram.fsm.state import StatesGroup, State

class PaymentState(StatesGroup):
    waiting_for_receipt = State()  # Ожидаем фото/файл с чеком
    user_details = State()  # Реквизиты пользователя