async def display_available_exchanges():

    from db.models.models import Partners

    text = (
        'Поддерживаются обмены:\n\n'
    )

    # Получаем все доступные обмены
    all_currencies = []
    partners_info = await Partners.filter(status=True)

    # Если нет партнёров - нет обменов
    if not partners_info:
        text = '❕ В данный момент обменов нет!'
        return text
    
    # Добавляемм обмены
    for info in partners_info:
        active_pairs = info.active_pairs
        for currencies in active_pairs:
            all_currencies.append([currencies.get('from', ''), currencies.get('to', '')])

    # Получаем уникальные строки в формате "XXX - YYY"
    unique_strings = set(f"{a} - {b}" for a, b in all_currencies)
    text += '\n'.join(unique_strings)
    text += '\n\nВыберите направление обмена'

    return text


async def partner_information(currency: str, id: int):

    from db.models.models import Partners, Exchanges, Rates

    rate_info = await Rates.get(id=id)
    partner_info = await Partners.get(tg_id=rate_info.partner_id)
    count_exchanges = await Exchanges.get_deal_count_by_partner(partner_id=rate_info.partner_id)

    text = (
        f'Выбран партнёр: {partner_info.name}\n'
        f'Совершенно обменов: {count_exchanges}\n'
        f'Курс: 1 CNY = {rate_info.rate} {currency}'
    )

    return text, rate_info.partner_id


async def confirmation_amount(currency: str, id: int):

    from db.models.models import Rates
    rate_info = await Rates.get(id=id)

    currencies_text = {
        'RUB': 'рублей',
        'USDT': 'долларов',
    }

    return f'Введите сумму для обмена в диапазоне {rate_info.limits} {currencies_text.get(currency, '')}', rate_info.limits


incorrect_data = ['❗ Введите число, сумма которой положительная', '❗ Пожалуйста, введите корректную сумму числом', '❗ Пожалуйста, введите число в нужном диапазоне: ']


async def format_exchange_message(sum: float, currency: str, platform: str, id: int, partner_id: int) -> str:

    from db.models.models import Rates, Partners

    rate_info = await Rates.get(id=id)
    partner = await Partners.get(tg_id=partner_id)

    cny_sum = round(sum/rate_info.rate)
    result = (
        f"\nВы отдаёте {sum} {currency.upper()}\n"
        f"для получения {cny_sum} CNY на {platform.capitalize()}\n\n"
        "❗️ ВНИМАНИЕ ❗️\n"
        f'Партнёр "{partner.name}" сейчас получит вашу заявку на обмен.\n'
        "Все сделки в боте застрахованы на сумму до 500 000 руб.\n\n"
        "⚠️ Будьте максимально внимательны при оплате!\n"
        "Если вы:\n"
        "• переведёте на другой банк,\n"
        "• укажете другое ФИО,\n"
        "• разобьёте платёж на части,\n"
        "• задержите оплату без согласования с партнёром —\n"
        "<b>деньги будут потеряны.</b>\n"
        "❌ Поддержка не сможет их вернуть.\n\n"
        "🔁 При повторных обменах всегда запрашивайте новые реквизиты — старые могут быть неактуальны!"
    )


    return result, cny_sum

async def format_exchange_request(amount: float, currency: str, platform: str, cny_sum: int) -> str:

    return (
        "Новая заявка на обмен:\n\n"
        f"Клиент отдаёт: {amount} {currency.upper()}\n"
        f"За: {cny_sum} CNY\n"
        f"Платформа: {platform}\n\n"
        f"Нажмите ниже, чтобы отправить клиенту реквизиты и условия оплаты ⬇️"
    )


def format_log_message(tg_id: int, currency: str, sum_amount: float) -> str:
    return f"📝 Новая заявка от клиента {tg_id}. Направление: {currency} → CNY. Сумма: {sum_amount} {currency}"

async def waiting_for_payment_mess(partner_id: int) -> str:

    from db.models.models import Partners

    partner = await Partners.get(tg_id=partner_id)
    text = (
        f"Партнёр {partner.name} получил вашу заявку на обмен и уже готовит реквизиты – пожалуйста, ожидайте. "
        "Обычно реквизиты отправляются в чат в течение 15 минут, если этого не произошло – сделка отменится автоматически.\n\n"
        "❗️ Внимание! После получения реквизитов у вас будет 15 минут на оплату сделки, поэтому будьте на связи! ❗️"
    )
    return text
