from settings import settings

from db.models.models import Users, Partners


# Добавление админов
async def register_initial_users():

    # Добавляем всех админов
    for admin_id in settings.bot.ADMINS:
        user_info = await Users.get(tg_id=admin_id)
        if not user_info:
            await Users.create(
                tg_id=admin_id,
                role='admin'
            )
            print(f'Новый админ: {admin_id}')

    # Добавляем всех партнёров
    for partner in settings.bot.PARTNERS:
        partner_id = partner.get('tg_id')
        user_info = await Users.get(tg_id=partner_id)
        if not user_info:
            await Users.create(
                tg_id=partner_id,
                role='partner'
            )

            await Partners.create(
                tg_id=partner_id,
                name=partner.get("name", "Без имени"),
                active_pairs=partner.get("active_pairs", [])
            )
            print(f'Новый партнёр: {partner_id}')