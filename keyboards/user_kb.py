from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


start_kb = [
    [types.KeyboardButton(text="\U0001F4D1 Выслать меню"),
    types.KeyboardButton(text="\U0001F32D Сделать заказ")]
]

start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=start_kb,
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)

back_kb = [
    [types.KeyboardButton(text="\U0001F4D1 Выслать меню"),
    types.KeyboardButton(text="\U0001F51D Вернутся к разделам")]
]

back_keyboard = types.ReplyKeyboardMarkup(
    keyboard=back_kb,
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)


def make_sections_keyboard(items: list[str]) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.add(types.KeyboardButton(text=str(item)))
    builder.adjust(3)
    builder.add(types.KeyboardButton(text="\U0001F519 Назад"))
    builder.add(types.KeyboardButton(text="\U0001F680 Завершить заказ"))
    builder.adjust(2)

    user_keyboard = builder.as_markup(
        resize_keyboard=True,
    )

    return user_keyboard


def make_food_keyboard(items: list[str]) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.add(types.KeyboardButton(text=str(item)))
    builder.adjust(3)
    builder.add(types.KeyboardButton(text="\U0001F51D В другой раздел меню"))
    builder.add(types.KeyboardButton(text="\U0001F680 Завершить заказ"))
    builder.adjust(2)

    user_keyboard = builder.as_markup(
        resize_keyboard=True,
    )

    return user_keyboard
