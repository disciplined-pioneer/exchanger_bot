exchange_completed_message = '✅ Вы завершили обмен!'

def exchange_completed_message_partner(user_id: int, id_exchange: int):
    return f'✅ Обмен №{id_exchange} был успешно завершён пользователем: {user_id}'

def format_message_to_partner(tg_id: int, user_text: str) -> str:
    return (
        f'Сообщение от клиента {tg_id}:\n\n'
        f'<b>"{user_text}"</b>\n\n'
        'Чтобы ответить, нажмите на кнопку "Ответить" и введите текст, иначе, сообщение не отправится'
    )

def confirmation_message() -> str:
    return 'Сообщение было отправлено продавцу'

def prompt_message_to_seller() -> str:
    return 'Напишите сообщение продавцу'
