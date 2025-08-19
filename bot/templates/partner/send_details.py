async def create_payment_message(details: str, sum: str, currency: str) -> str:
    return (
        f"Реквизиты для оплаты:\n"
        f"{details}\n\n"
        f"Оплатите {sum} в {currency} по указанным реквизитам и нажмите кнопку ниже, когда завершите.\n\n"
        f"❗️ Внимание! У вас есть 15 минут на оплату этой сделки, через 15 минут она отменится автоматически и реквизиты для оплаты будут не актуальны – "
        f"ВЫ НЕ СМОЖЕТЕ ВЕРНУТЬ СВОИ ДЕНЬГИ В СЛУЧАЕ ЗАДЕРЖКИ ОПЛАТЫ!"
    )

input_requisites_message = 'Введите свои реквизиты в формате текста. Иной формат не будет принят:'


def get_confirm_requisites_message(details_text):
    return f"Подтвердите реквизиты:\n\n{details_text}"

requisites_sent_message = '✅ Реквизиты были отправлены. Ожидайте оплату и квитанцию'

enter_requisites_message = '❗️ Пожалуйста, введите реквизиты в формате текста'

error_message_text = "❗️ Пожалуйста, используйте кнопку для отправки реквизитов"