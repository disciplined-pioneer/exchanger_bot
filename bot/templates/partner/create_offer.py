direction_input = 'Введите направление'

def generate_announcement_message(platform, currency):
    currency_display = 'рублях' if currency.upper() == 'RUB' else currency
    return f'Вы выбрали направление: {platform} > {currency}\nВведите лимиты объявления в {currency_display} в формате 100-500 (диапазон)'


def exchange_rate_message(currency):
    return f"Напишите курс обмена, сколько нужно заплатить {currency.upper()}, чтобы получить 1 CNY"

def create_advertisement_message(platform, currency, limits, exchange_rate):
    return (
        f'✅ Ваше объявление создано\n'
        f'Направление: {platform} > {currency}\n'
        f'Лимиты: {limits}\n'
        f'Курс: 1 CNY = {exchange_rate} {currency}\n'
    )

def format_partner_rate_log(tg_id, currency, platform, limits, exchange_rate) -> str:
    return (
        f'🔄 Партнёр {tg_id} добавил курс:\n'
        f'Обмен: {currency}-{platform} / {limits} {currency}. Курс: {exchange_rate}'
    )
