async def create_payment_message(details: str, sum: str, currency: str) -> str:
    return (
        f"Реквизиты для оплаты:\n"
        f"{details}\n\n"
        f"Оплатите {sum} в {currency} "
        f"по указанным реквизитам и нажмите кнопку ниже, когда завершите."
    )


input_requisites_message = 'Введите свои реквизиты:'


def get_confirm_requisites_message(details_text):
    return f"Подтвердите реквизиты:\n\n{details_text}"

requisites_sent_message = '✅ Реквизиты были отправлены. Ожидайте оплату и квитанцию'

enter_requisites_message = '❗️ Пожалуйста, введите реквизиты в формате текста'

error_message_text = "❗️ Пожалуйста, используйте кнопку для отправки реквизитов"