from core.bot import bot
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, Message

from db.models.models import ExchangeHistory
from bot.keyboards.admin.broadcast import *
from bot.templates.admin.broadcast import *
from utils.admin.broadcast import create_url_keyboard, remove_urls, send_preview


router = Router()


# Обработка рассылки
@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BroadcastStates.waiting_for_content)
    sent_message = await callback.message.edit_text("📨 Отправьте сообщение для рассылки (для отправки фото или документа вместе с текстом, отправьте их в одном сообщении):",
                                     reply_markup=cancel_keyboard())
    
    # Сохраняем message_id последнего сообщения бота
    await state.update_data(last_bot_message_id=sent_message.message_id)


# Обрабатыавем сообщениие админа
@router.message(BroadcastStates.waiting_for_content, F.content_type.in_(["text", "photo", "video", "document", "audio"]))
async def handle_content(message: Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")

    content_data = {
        "msg_type": message.content_type,
        "file_id": None,
        "caption": message.caption or message.text or "",
        "parse_mode": None,
        "keyboard": []
    }

    if message.content_type != "text":
        if message.content_type == "photo":
            content_data["file_id"] = message.photo[-1].file_id
        else:
            content_data["file_id"] = getattr(message, message.content_type).file_id

    # Редактируем предыдущее сообщение бота
    try:
        sent_message = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_bot_message_id,
            text="Выберите форматирование:",
            reply_markup=format_selection_keyboard()
        )
    
        # Обновляем ID последнего сообщения бота
        await state.update_data(broadcast=content_data,
                                last_bot_message_id=sent_message.message_id)
    except:
        pass


# Обработка типа форматирования
@router.callback_query(F.data.startswith("set_mode:"))
async def set_parse_mode(callback: types.CallbackQuery, state: FSMContext):
    mode = callback.data.split(":")[1]
    data = await state.get_data()
    content = data["broadcast"]
    content["parse_mode"] = None if mode == "None" else mode
    await state.update_data(broadcast=content)

    await callback.message.delete()
    await callback.message.answer("Вот как будет выглядеть сообщение:")
    await send_preview(callback.message, content, content["parse_mode"])
    await callback.message.answer("Добавить кнопки или подтвердить рассылку:", reply_markup=preview_keyboard())


# Добавление url кнопок
@router.callback_query(F.data == "add_buttons")
async def ask_buttons(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Отправьте кнопки в формате:\n\nКупить - https://site.ru | Каталог - https://site.ru/catalog",
        reply_markup=cancel_keyboard()
    )
    await state.set_state(BroadcastStates.waiting_for_buttons)
    await callback.answer()


# Выводим сообщение рассылки админа
@router.message(BroadcastStates.waiting_for_buttons)
async def handle_buttons(message: Message, state: FSMContext):

    try:
        await message.delete()
        data = await state.get_data()
        content = data["broadcast"]

        buttons = []
        for row in message.text.split("\n"):
            row_buttons = []
            try:
                for pair in row.split("|"):
                    text, url = map(str.strip, pair.split("-", 1))
                    row_buttons.append(InlineKeyboardButton(text=text, url=url))
            except:
                pass
            buttons.append(row_buttons)

        content["keyboard"] = buttons
        await state.update_data(broadcast=content)
        await message.answer("Превью с кнопками:")
        await send_preview(message, content, content["parse_mode"])
        await message.answer("Готово к отправке?", reply_markup=confirm_keyboard())
    except:
        pass


# Подтверждение рассылки
@router.callback_query(F.data == "confirm_send")
async def confirm_broadcast(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    content = data["broadcast"]
    parse_mode = content.get("parse_mode")

    parse_mode = parse_mode

    user_topics = await ExchangeHistory.all()
    user_ids = list(set([u.tg_id for u in user_topics]))

    for user_id in user_ids:
        try:
            markup = create_url_keyboard(content["caption"], content.get("keyboard", []))
            caption = remove_urls(content["caption"])
            if content["msg_type"] == "text":
                await callback.bot.send_message(user_id, caption, parse_mode=parse_mode, reply_markup=markup)
            elif content["msg_type"] == "photo":
                await callback.bot.send_photo(user_id, content["file_id"], caption=caption, parse_mode=parse_mode, reply_markup=markup)
            elif content["msg_type"] == "video":
                await callback.bot.send_video(user_id, content["file_id"], caption=caption, parse_mode=parse_mode, reply_markup=markup)
            elif content["msg_type"] == "audio":
                await callback.bot.send_audio(user_id, content["file_id"], caption=caption, parse_mode=parse_mode, reply_markup=markup)
            elif content["msg_type"] == "document":
                await callback.bot.send_document(user_id, content["file_id"], caption=caption, parse_mode=parse_mode, reply_markup=markup)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user_id}: {e}")

    await callback.message.edit_text("✅ Рассылка успешно завершена")
    await state.clear()


# Отмена рассылки
@router.callback_query(F.data == "cancel")
async def cancel_action(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Рассылка была отменена")
    await state.clear()


