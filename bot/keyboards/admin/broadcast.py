from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Меню", callback_data="go_back_menu")]
    ]
)


def cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")
    ]])


def preview_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Добавить url-кнопки", callback_data="add_buttons")
    ], [
        InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_send"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")
    ]])


def confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_send"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")
    ]])


def format_selection_keyboard():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="HTML", callback_data="set_mode:HTML")],
        [InlineKeyboardButton(text="Markdown", callback_data="set_mode:Markdown")],
        [InlineKeyboardButton(text="Без форматирования", callback_data="set_mode:None")]
    ])
