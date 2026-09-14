# 💱 Обменник Бот обменник

Телеграм-бот для обмена валют с поддержкой трёх ролей: **Админ**, **Партнёр**, **Пользователь**.

## 📌 Возможности

### 👤 Пользователь
- Запрашивает обмен валют
- Указывает желаемую сумму, валюту и реквизиты
- Получает подтверждение от партнёра

### 🤝 Партнёр
- Изменяет текущий курс обмена
- Обрабатывает заявки пользователей
- Отправляет результат обмена

### 🛠 Админ
- Просматривает статистику всех обменов
- Отправляет массовые сообщения пользователям (рассылки)

---

## ⚙️ Настройка окружения

Перед запуском необходимо создать файл `.env` в корне проекта со следующими переменными:

```env
# Данные для подключения к PostgreSQL
POSTGRES_NAME=your_database_name
POSTGRES_HOST=your_host
POSTGRES_PORT=your_port
POSTGRES_PASSWORD=your_password
POSTGRES_USER=your_user

# Токен Telegram-бота
BOT_TOKEN=your_telegram_bot_token
BOT_GROUP_ID=id вашей группы с '-'
BOT_COMMISSION=в процентах (0.2)

# ID админов 
BOT_ADMINS=[admin_telegram_ids]
BOT_PARTNERS=[{"tg_id": 123456789, "name": "Иван", "active_pairs": [{"from": "USDT", "to": "CNY", "platform": "Wechat"}]}]

# Ссылка на поддержку (можно заменить на ваш сайт или Telegram-юзер)
BOT_SUPPORT_LINK=https://your_support_link
```

## Статусы в истории сообщений

- обмен начат → exchange_started
- ожидание подтверждения оплаты → waiting_for_payment_confirmation
- оплата не получена → payment_not_received
- обмен завершён → exchange_completed


---

## 🗂 Структура проекта

```
├─── bot
│   ├─── handlers
│   │   ├─── admin
│   │   │   ├─── add_partner.py 
│   │   │   ├─── ban.py
│   │   │   ├─── broadcast.py   
│   │   │   ├─── commissions.py 
│   │   │   └─── statistics.py  
│   │   ├─── partner
│   │   │   ├─── create_offer.py
│   │   │   ├─── my_offers.py
│   │   │   ├─── reply_to_user.py
│   │   │   ├─── result_exchange.py
│   │   │   ├─── send_details.py
│   │   │   ├─── statistics.py
│   │   │   └─── view_requests.py
│   │   ├─── user
│   │   │   ├─── clear_state.py
│   │   │   ├─── exchange_confirmation.py
│   │   │   ├─── exchange_currency.py
│   │   │   ├─── start.py
│   │   │   └─── user_details.py
│   │   └─── __init__.py
│   ├─── keyboards
│   │   ├─── admin
│   │   │   ├─── add_partner.py
│   │   │   ├─── ban.py
│   │   │   ├─── broadcast.py
│   │   │   └─── commissions.py
│   │   ├─── partner
│   │   │   ├─── create_offer.py
│   │   │   ├─── my_offers.py
│   │   │   ├─── reply_to_user.py
│   │   │   ├─── result_exchange.py
│   │   │   ├─── send_details.py
│   │   │   ├─── statistics.py
│   │   │   └─── view_requests.py
│   │   ├─── user
│   │   │   ├─── exchange_confirmation.py
│   │   │   ├─── exchange_currency.py
│   │   │   ├─── start.py
│   │   │   └─── user_details.py
│   │   └─── __init__.py
│   ├─── templates
│   │   ├─── admin
│   │   │   ├─── add_partner.py
│   │   │   ├─── ban.py
│   │   │   ├─── broadcast.py
│   │   │   ├─── commissions.py
│   │   │   └─── statistics.py
│   │   ├─── partner
│   │   │   ├─── create_offer.py
│   │   │   ├─── my_offers.py
│   │   │   ├─── result_exchange.py
│   │   │   ├─── send_details.py
│   │   │   ├─── statistics.py
│   │   │   └─── view_requests.py
│   │   ├─── user
│   │   │   ├─── exchange_confirmation.py
│   │   │   ├─── exchange_currency.py
│   │   │   ├─── start.py
│   │   │   └─── user_details.py
│   │   └─── __init__.py
│   └─── __init__.py
├─── core
│   ├─── __init__.py
│   ├─── bot.py
│   └─── psql.py
├─── db
│   ├─── crud
│   │   ├─── __init__.py
│   │   └─── base.py
│   ├─── models
│   │   ├─── mapped_columns.py
│   │   └─── models.py
│   └─── __init__.py
├─── services
│   ├─── init_users.py
│   └─── report_timer.py
├─── utils
│   ├─── admin
│   │   ├─── add_partner.py
│   │   ├─── ban.py
│   │   ├─── broadcast.py
│   │   └─── commissions.py
│   ├─── partner
│   │   ├─── create_offer.py
│   │   ├─── my_offers.py
│   │   └─── result_exchange.py
│   └─── user
│       ├─── exchange_confirmation.py
│       ├─── exchange_currency.py
│       ├─── request_details.py
│       ├─── start.py
│       └─── user_details.py
├─── .env
├─── .gitignore
├─── Dockerfile
├─── README.md
├─── bot.py
├─── docker-compose.yml
├─── requirements.txt
└─── settings.py
```

---

## 🚀 Быстрый старт

```bash
# Клонируем проект
git clone https://github.com/your/repo.git
cd your-repo

# Создаём .env и заполняем его

# Устанавливаем зависимости
pip install -r requirements.txt

# Запуск бота
python bot.py
```

Или с помощью Docker:

```bash
docker-compose up --build
```

---

## 🧪 Генерация тестовых данных

Файл `test.py` используется для генерации фейковых данных обменов в базе данных — удобно для тестирования и отладки.

```bash
python test.py
```

---
