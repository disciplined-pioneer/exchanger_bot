photo_or_receipt_message = "Пожалуйста, отправьте фото или файл с чеком в этот чат"

payment_confirmation_message = "Клиент подтвердил оплату и отправил чек:"

photo_or_document_request_message = "❗️ Пожалуйста, отправьте фото или документ"


def generate_requisites_message(platform: str=''):
    return f"Введите свои реквизиты:\n{platform}. Или загрузите QR-код для оплаты"


photo_document_or_text_request_message = "❗️ Пожалуйста, отправьте фото, документ или текст"

complete_deal_instruction_msg = "Если деньги вам всё-таки пришли, то вы можете завершить сделку самостоятельно"

def generate_payment_message(sum: float, data: str='') -> str:

    return f"Ожидайте зачисления:\n\nСумма: {sum}\n{data}"


def format_confirm_details(details: str='') -> str:
    return f"Подтвердите отправку реквизитов: {details}"


def get_no_payment_instructions() -> str:
    return (
        "Прошло уже 15 минут, обычно деньги приходят раньше. Возможно, что-то пошло не так. Но вы можете написать партнеру. Если не удалось решить с партнером – пишите в поддержку. Если все решено и деньги уже получены – нажимайте кнопку «назад» и завершите сделку"
    )


def format_user_details(details: str='') -> str:
    return f"Реквизиты пользователя:\n{details}"


def format_receipt_log(tg_id: int, id_exchange: int) -> str:
    return f"📎 Клиент {tg_id} отправил чек по заявке {id_exchange}"

async def format_seller_message(tg_id, message_text):

    from db.models.models import Partners

    partner = await Partners.get(tg_id=tg_id)
    return (
        f'Сообщение от продавца {partner.name}:\n\n'
        f'<b>"{message_text}"</b>\n\n'
        'Чтобы ответить, нажмите на кнопку "Ответить" и введите текст, иначе, сообщение не отправится'
    )

def get_sent_confirmation():
    return 'Сообщение было отправлено пользователю'

def generate_client_message_text(user_id):
    return f'Напишите сообщение клиенту: {user_id}'
