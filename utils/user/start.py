from db.models.models import Users

# Фукнция для проверки наличия пользователя в БД и его статуса на Бан
async def check_ban_status(user_id: int):
    
    user_info = await Users.get(tg_id=user_id)

    # Если есть, проверяем роль
    if user_info:
        if user_info.role == 'ban':
            return True, 'ban'
        else:
            return False, user_info.role
        
    # Если нет, то добавляем id
    else:
        await Users.create(
            tg_id=user_id,
            role='client'
        )
        return False, 'client'