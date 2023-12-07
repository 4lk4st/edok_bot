import os
from aiogram import types, Router, F
from aiogram.filters.command import CommandStart

from keyboards import food_keyboard, start_keyboard, monday_menu
from create_bot import bot


router = Router()


@router.message(CommandStart())
async def command_start(
    message: types.Message,
) -> None:
    await message.answer("Привет! Ты можешь посмотреть меню или сделать заказ!",
                         reply_markup=start_keyboard)


@router.message(F.text.lower() == "выслать меню")
async def command_food(
    message: types.Message,
) -> None:
    document = types.FSInputFile("data/menu_example.pdf", filename="menu.pdf")
    await bot.send_document(chat_id=message.chat.id, document=document)
    await message.answer("Вот актуальное меню!",
                         reply_markup=start_keyboard)


@router.message(F.text.lower() == "сделать заказ")
async def command_food(
    message: types.Message,
) -> None:
    await message.answer("Чтобы сделать заказ, выбери блюдо!",
                         reply_markup=food_keyboard)


@router.message(F.text.in_(list(monday_menu.keys())))
async def command_food(
    message: types.Message,
) -> None:
    await message.answer("Заказ принят!",
                         reply_markup=types.ReplyKeyboardRemove())
