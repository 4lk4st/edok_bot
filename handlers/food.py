import json

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import (make_sections_keyboard, make_food_keyboard,
                        start_keyboard, get_menu_sections,
                        get_food_list, get_all_food, back_keyboard)
from create_gsheet import write_to_gsheet

from handlers.services import add_food_to_order, send_order_info_to_chat


router = Router()

class OrderFood(StatesGroup):
    choosing_section = State()
    choosing_food = State()


@router.message(F.text.lower() == "сделать заказ")
@router.message(F.text.lower() == "вернутся к разделам")
async def open_menu_kb(
    message: types.Message,
    state: FSMContext
) -> None:
    await message.answer(
        "Чтобы сделать заказ, выбери раздел меню!",
        reply_markup=make_sections_keyboard(get_menu_sections())
    )
    await state.set_state(OrderFood.choosing_section)


@router.message(
    OrderFood.choosing_section,
    F.text.in_(get_menu_sections())
)
async def open_menu_kb(
    message: types.Message,
    state: FSMContext
) -> None:
    await state.update_data(
        {"current_section": f"{message.text}"}
    )
    get_all_data = await state.get_data()
    get_current_section = get_all_data["current_section"]
    await message.answer(
        "Чтобы сделать заказ, нажми на кнопку блюда!",
        reply_markup=make_food_keyboard(get_food_list(get_current_section))
    )
    await state.set_state(OrderFood.choosing_food)


@router.message(
    OrderFood.choosing_food,
    F.text.in_(get_all_food())
)
async def choose_food(
    message: types.Message,
    state: FSMContext
) -> None:
    food = message.text.lower()
    await add_food_to_order(food, state)
    
    final_order_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали: {json.dumps(final_order_data, ensure_ascii=False)}."
    )
    get_all_data = await state.get_data()
    get_current_section = get_all_data["current_section"]
    await message.answer(
        text=("Добавьте ещё блюдо в заказ, перейдите в другой раздел меню, " 
              "или завершите заказ!"),
        reply_markup=make_food_keyboard(get_food_list(get_current_section))
    )


@router.message(
    F.text.lower() == "завершить заказ")
async def send_order(
    message: types.Message,
    state: FSMContext
) -> None:
    await send_order_info_to_chat(message, state)   
    await write_to_gsheet(message, state)

    await state.clear()

    await message.answer(
        text=("Для формирования нового заказа нажмите или введите /start"),
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(
    OrderFood.choosing_food,
    F.text.lower() == "в другой раздел меню")
async def another_section(
    message: types.Message,
    state: FSMContext
) -> None:
    await message.answer(
        "Чтобы сделать заказ, выбери раздел меню!",
        reply_markup=make_sections_keyboard(get_menu_sections())
    )
    await state.set_state(OrderFood.choosing_section)


@router.message(
    F.text.lower() == "назад")
async def command_back(
    message: types.Message,
) -> None:
    await message.answer("Ты можешь посмотреть меню или вернутся к разделам!",
                         reply_markup=back_keyboard)
