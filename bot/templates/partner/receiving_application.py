

async def create_payment_message(details: str, sum: str, currency: str) -> str:
    return (
        f"Реквизиты для оплаты:\n"
        f"{details}\n\n"
        f"Оплатите {sum} в {currency} "
        f"по указанным реквизитам и нажмите кнопку ниже, когда завершите."
    )
