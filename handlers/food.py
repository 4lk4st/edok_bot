import json
from datetime import date, datetime, timedelta

from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import make_row_keyboard, start_keyboard, menu
from create_bot import bot
from create_gsheet import write_to_gsheet


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
async def send_menu(
    message: types.Message,
) -> None:
    document = types.FSInputFile("data/menu_example.pdf", filename="menu.pdf")
    await bot.send_document(chat_id=message.chat.id, document=document)
    await message.answer("Вот актуальное меню!",
                         reply_markup=start_keyboard)


@router.message(StateFilter(None), F.text.lower() == "сделать заказ")
async def open_menu_kb(
    message: types.Message,
    state: FSMContext
) -> None:
    await message.answer(
        "Чтобы сделать заказ, выбери блюдо!",
        reply_markup=make_row_keyboard(list(menu.keys()))
    )
    
    await state.set_state(OrderFood.choosing_food)


@router.message(
    OrderFood.choosing_food,
    F.text.in_(list(menu.keys())))
async def choose_food(
    message: types.Message,
    state: FSMContext
) -> None:
    
    food = message.text.lower()
    current_order_data = await state.get_data()
    if food not in current_order_data:
        await state.update_data(
            {f"{food}": 1}
        )
    else:
        current_quantity = current_order_data[food]
        await state.update_data(
            {f"{food}": current_quantity + 1}
        )
    
    final_order_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали: {json.dumps(final_order_data, ensure_ascii=False)}."
    )
    await message.answer(
        text=("Добавление блюд в заказ - кнопка с соответствующим блюдом, " 
              "завершение заказа - кнопка 'Завершить заказ'"),
        reply_markup=make_row_keyboard(list(menu.keys()))
    )

@router.message(
    OrderFood.choosing_food,
    F.text.lower() == "завершить заказ")
async def send_order(
    message: types.Message,
    state: FSMContext
) -> None:
    order_data = await state.get_data()
    order_str = str(json.dumps(order_data, ensure_ascii=False))
    await message.answer(
        text=(f"Ваш заказ: {order_str} "
               "направлен администратору."),
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    current_utctime = datetime.utcnow() + timedelta(hours=7)
    write_to_gsheet(current_date = str(date.today()),
                    current_tomsk_time = current_utctime.strftime("%H:%M"),
                    user_name = f"{message.from_user.last_name} {message.from_user.first_name}",
                    order_str = order_str
    )

    await state.clear()
