from settings import settings
from db.models.models import Partners

async def commission_info_message():
    count_partners = len(await Partners.all())
    return f'Комиссия к получению: {settings.bot.COMMISSION} CNY\nПартнёров: {count_partners}'


def commission_payment_message():
    return f'Вам надо заплатить комиссию суммой {settings.bot.COMMISSION} CNY'

messages_sent_message = '✅ Сообщения были отправлены партнёрам'

payment_confirmed_message = '✅ Вы подтвердили оплату'

async def partner_paid_commission_message(tg_id):
    partner = await Partners.get(tg_id=tg_id)
    return f'Партнёр:\nID: {tg_id}, Имя: {partner.name}\nОплатил комиссию в размере {settings.bot.COMMISSION} CNY'
