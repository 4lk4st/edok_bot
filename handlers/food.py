import os
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import make_row_keyboard, start_keyboard, monday_menu
from create_bot import bot


router = Router()

class OrderFood(StatesGroup):
    choosing_food = State()


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


@router.message(StateFilter(None), F.text.lower() == "сделать заказ")
async def command_food(
    message: types.Message,
    state: FSMContext
) -> None:
    await message.answer(
        "Чтобы сделать заказ, выбери блюдо!",
        reply_markup=make_row_keyboard(list(monday_menu.keys()))
    )
    
    await state.set_state(OrderFood.choosing_food)


@router.message(
    OrderFood.choosing_food,
    F.text.in_(list(monday_menu.keys())))
async def command_food(
    message: types.Message,
    state: FSMContext
) -> None:
    await state.update_data(chosen_food=message.text.lower())
    order_data = await state.get_data()
    await message.answer(
        text=f"Ваш заказ: {order_data['chosen_food']}.",
        reply_markup=make_row_keyboard(list(monday_menu.keys()))
    )
    # await message.answer("Заказ принят!",
    #                      reply_markup=types.ReplyKeyboardRemove())
