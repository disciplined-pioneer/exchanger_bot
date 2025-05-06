photo_or_receipt_message = "Пожалуйста, отправьте фото или файл с чеком в этот чат"

payment_confirmation_message = "Клиент подтвердил оплату и отправил чек:"

photo_or_document_request_message = "❗️ Пожалуйста, отправьте фото или документ"


def generate_requisites_message(platform: str=''):
    return f"Введите свои реквизиты:\n{platform}. Или загрузите QR-код для оплаты"


photo_document_or_text_request_message = "❗️ Пожалуйста, отправьте фото, документ или текст"


def generate_payment_message(sum: float, data: str='') -> str:

    return f"Ожидайте зачисления:\n\nСумма: {sum}\nРеквизиты:\n{data}"


def format_confirm_details(details: str='') -> str:
    return f"Подтвердите отправку реквизитов: {details}"


def get_no_payment_instructions(partner_id: int) -> str:
    return (
        "Если не пришли деньги:\n\n"
        f"1\\. Напишите в чат партнеру: [связаться](tg://user\\?id\\={partner_id})\n\n"
        "2\\. Если нет ответа 3 часа и более, напишите в поддержку\\."
    )


def format_user_details(details: str='') -> str:
    return f"Реквизиты пользователя:\n{details}"

