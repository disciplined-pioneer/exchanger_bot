choose_ad_message = 'Выберите нужное объявление'

def get_rate_info_text(rate_info):
    return (
        f'Стоимость: 1 {rate_info.to_currency} = {rate_info.rate} {rate_info.from_currency}\n'
        f'Лимиты: {rate_info.limits}'
    )

rate_deleted_message = '✅ Ваш курс был успешно удалён!'

rate_not_found_message = '⚠️ Курс не найден или уже удалён'

def get_payment_prompt(rate):
    return f'Введите сколько надо заплатить {rate.from_currency} за 1 {rate.to_currency}'

rate_updated_message = '✅ Курс был успешно изменён!'
