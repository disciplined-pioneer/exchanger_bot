exchange_completed_message = '✅ Вы завершили обмен!'

def exchange_completed_message_partner(user_id: int, id_exchange: int):
    return f'✅ Обмен №{id_exchange} был успешно завершён пользователем: {user_id}'