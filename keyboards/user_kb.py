from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from .data import monday_menu

builder = ReplyKeyboardBuilder()
for i in list(monday_menu.keys()):
    builder.add(types.KeyboardButton(text=str(i)))
builder.adjust(3)

# user_keyboard = types.ReplyKeyboardMarkup(
#     keyboard=kb,
#     resize_keyboard=True,
#     input_field_placeholder="Выбери блюдо"
# )

user_keyboard = builder.as_markup(
    resize_keyboard=True,
    input_field_placeholder="Выбери блюдо"
)
