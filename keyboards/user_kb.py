from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


start_kb = [
    [types.KeyboardButton(text="Выслать меню"),
    types.KeyboardButton(text="Сделать заказ")]
]

start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=start_kb,
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)

def make_row_keyboard(items: list[str]) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.add(types.KeyboardButton(text=str(item)))
    builder.adjust(3)
    builder.add(types.KeyboardButton(text="В другой раздел меню"))
    builder.add(types.KeyboardButton(text="Завершить заказ"))
    builder.adjust(2)
    

    user_keyboard = builder.as_markup(
        resize_keyboard=True,
    )

    return user_keyboard