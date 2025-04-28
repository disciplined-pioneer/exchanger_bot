import asyncio
from datetime import datetime
from db.models.models import ExchangeHistory
from db.crud.base import init_postgres

async def fill_exchange_history():
    """
    Заполняем таблицу ExchangeHistory примерными данными.
    """
    await ExchangeHistory.create(
        tg_id=802587774,
        partner_id=123,
        date=datetime(2025, 4, 1, 10, 0),  # Примерная дата
        cny_amount=100.0,
        currency_name='USD',
        currency_amount=12.0,
        status="exchange_started"
    )
    await ExchangeHistory.create(
        tg_id=802587774,
        partner_id=123,
        date=datetime(2025, 4, 10, 15, 30),  # Примерная дата
        cny_amount=150.0,
        currency_name='USD',
        currency_amount=18.0,
        status="exchange_completed"
    )
    await ExchangeHistory.create(
        tg_id=802587774,
        partner_id=123,
        date=datetime(2025, 4, 15, 9, 0),  # Примерная дата
        cny_amount=200.0,
        currency_name='RUB',
        currency_amount=1600.0,
        status="exchange_completed"
    )
    await ExchangeHistory.create(
        tg_id=802587774,
        partner_id=123,
        date=datetime(2025, 4, 20, 13, 45),  # Примерная дата
        cny_amount=120.0,
        currency_name='RUB',
        currency_amount=960.0,
        status="payment_not_received"
    )

async def main():

    # Инициализация PostgreSQL
    await init_postgres()

    # Заполняем таблицу ExchangeHistory
    await fill_exchange_history()

    # Получаем сумму для CNY за текущий месяц
    total_cny = await ExchangeHistory.get_cny_amount_current_month()
    print(f"Сумма CNY за текущий месяц: {total_cny}")

    # Получаем сумму для USD за текущий месяц
    usd_amount = await ExchangeHistory.get_currency_amount_for_month('USD')
    print(f"Сумма USD за текущий месяц: {usd_amount}")

    # Получаем сумму для RUB за текущий месяц
    rub_amount = await ExchangeHistory.get_currency_amount_for_month('RUB')
    print(f"Сумма RUB за текущий месяц: {rub_amount}")

if __name__ == "__main__":
    asyncio.run(main())
