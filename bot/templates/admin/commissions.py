
from db.models.models import Partners, Exchanges

async def commission_info_message():
    count_partners = await Exchanges.get_partners_with_debt_count()
    commissions = await Exchanges.get_total_unpaid_commission()
    return f'Комиссия к получению: {commissions} CNY\nПартнёров: {count_partners}'


async def commission_payment_message(commissions: int):
    return f'Оплатите комиссию сервиса в размере {commissions} юаней на следующие реквизиты (Alipay):\n\n7-9644307030\nVinogradov Aleksandr'


messages_sent_message = '✅ Сообщения были отправлены партнёрам'

payment_confirmed_message = '✅ Вы подтвердили оплату'

async def partner_paid_commission_message(tg_id, name, commissions):   
    return f'Партнёр:\nID: {tg_id}, Имя: {name}\nОплатил комиссию в размере {commissions} CNY'
