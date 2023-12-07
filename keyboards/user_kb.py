from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from .data import monday_menu

builder = ReplyKeyboardBuilder()
for i in list(monday_menu.keys()):
    builder.add(types.KeyboardButton(text=str(i)))
builder.adjust(3)

food_keyboard = builder.as_markup(
    resize_keyboard=True,
    input_field_placeholder="Выбери блюдо"
)


start_kb = [
    [types.KeyboardButton(text="Выслать меню"),
    types.KeyboardButton(text="Сделать заказ")]
]

start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=start_kb,
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)
