from settings import settings
from db.models.models import Partners, Exchanges

async def commission_info_message():
    count_partners = len(await Partners.all())
    commissions = await Exchanges.get_amout_to_current_month() * settings.bot.COMMISSION
    return f'Комиссия к получению: {commissions} CNY\nПартнёров: {count_partners}'


async def commission_payment_message():
    commissions = await Exchanges.get_amout_to_current_month() * settings.bot.COMMISSION
    return f'Оплатите комиссию сервиса в размере {commissions} юаней на следующие реквизиты (Alipay):\n\n7-9644307030\nVinogradov Aleksandr'


messages_sent_message = '✅ Сообщения были отправлены партнёрам'

payment_confirmed_message = '✅ Вы подтвердили оплату'

async def partner_paid_commission_message(tg_id):
    partner = await Partners.get(tg_id=tg_id)    
    commissions = await Exchanges.get_amout_to_current_month() * settings.bot.COMMISSION
    return f'Партнёр:\nID: {tg_id}, Имя: {partner.name}\nОплатил комиссию в размере {commissions} CNY'
