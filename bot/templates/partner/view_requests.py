choose_request_message = 'Выберите нужную заявку'

def get_transaction_details(platform, from_currency, to_currency, amount_to, amount_from, state):
    return (
        f'Направление: {platform} > {from_currency}\n'
        f'Сумма {to_currency}: {amount_to}\n'
        f'Сумма {from_currency}: {amount_from}\n'
        f'Статус: {state}'
    )
