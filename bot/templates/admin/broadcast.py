from aiogram.fsm.state import State, StatesGroup

class BroadcastStates(StatesGroup):
    waiting_for_content = State()
    waiting_for_buttons = State()

access_denied_message = "❌ Вам отказано в доступе"

broadcast_prompt_message = "Отправь текст или файл для рассылки:"

choose_format_message = "Выбери форматирование: Markdown или HTML"

enter_caption_message = "Введи подпись (или '-' если без подписи):"

broadcast_complete_message = "✅ Ваш рассылка успешно завершена!"

broadcast_cancelled_message = "❌ Вы отмененили рассылку"
