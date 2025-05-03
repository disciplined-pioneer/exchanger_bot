from db.models.models import Partners, Users
from aiogram.fsm.state import StatesGroup, State

class AddPartner(StatesGroup):
    current_index = State()
    values = State()


PARTNER_QUESTIONS = {
    "telegram_id": "Введите Telegram ID партнёра",
    "name": "Введите имя партнёра"
}


# Добавление партнёра
async def adding_partner(tg_id: int, name: str):

    user = await Users.get(tg_id=tg_id)
    if user: # Если есть партнёр
        await user.update(role='partner')

    else: # Если нет партнёра
        await Users.create(
            tg_id=tg_id,
            role='partner'
        )

    # Сохранение в БД
    await Partners.create(
        tg_id=tg_id,
        name=name,
        active_pairs=[
            {'from': 'USDT', 'to': 'CNY', 'platform': 'WeChat'},
            {'from': 'USDT', 'to': 'CNY', 'platform': 'Alipay'},
            
            {'from': 'RUB', 'to': 'CNY', 'platform': 'Alipay'},
            {'from': 'RUB', 'to': 'CNY', 'platform': 'WeChat'}]
    )