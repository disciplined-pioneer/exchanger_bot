telegram_id_message = 'Введите Telegram_id пользователя для бана'

telegram_id_error_message = '❌ Telegram ID должен быть положительным числом!'

telegram_id_ban = '❌ Пользователь с этим ID уже забанен. Пожалуйста, введите другой ID'

def user_banned_message(tg_id):
    return f"✅ Пользователь с {tg_id} был забанен"
