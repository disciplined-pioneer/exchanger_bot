photo_or_receipt_message = "Пожалуйста, отправьте фото или файл с чеком в этот чат"

payment_confirmation_message = "Клиент подтвердил оплату и отправил чек:"

photo_or_document_request_message = "❗️ Пожалуйста, отправьте фото или документ"

def generate_requisites_message(exchange_type):
    return f"Введите свои реквизиты:\n{exchange_type}. Или загрузите QR-код для оплаты"

photo_document_or_text_request_message = "❗️ Пожалуйста, отправьте фото, документ или текст"


def generate_payment_message(sum: float, data: str='') -> str:

    return f"Ожидайте зачисления:\nСумма: {sum}\nРеквизиты:\n{data}"
