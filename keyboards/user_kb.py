from aiogram import types

from .data import monday_menu


kb = [[types.KeyboardButton(text=i) for i in list(monday_menu.keys())],]


user_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Выбери блюдо"
)
