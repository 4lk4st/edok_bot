import json

from aiogram import types
from aiogram.fsm.context import FSMContext


order_json_example = {
    "current_section": "Салаты",
    "Салаты": {
            "Оливье": 1,
            "Шанхай": 2
    },
    "Супы": {
            "Щи 500 мл": 3,
            "Тыквенный": 1
    },
    "current_price": 0
}

async def add_food_to_order(
    food:str,
    state: FSMContext
) -> None:
    current_order_data = await state.get_data()
    current_section = current_order_data["current_section"]

    if current_section not in current_order_data:
        await state.update_data(
            {current_section: {f"{food}": 1}}
        )
    elif ((current_section in current_order_data)
        and (food not in current_order_data[current_section])):
        current_order_data[current_section].update({f"{food}": 1})
        await state.set_data(current_order_data)
    else:
        current_quantity = current_order_data[current_section][food]
        current_order_data[current_section][food] = current_quantity + 1
        await state.set_data(current_order_data)


async def send_order_info_to_chat(
    message: types.Message,
    state: FSMContext   
) -> None:
    order_data = await state.get_data()
    order_data.pop("current_section")
    order_str = str(json.dumps(order_data, ensure_ascii=False))

    await message.answer(
        text=(f"Ваш заказ: {order_str} направлен администратору."),
        reply_markup=types.ReplyKeyboardRemove()
    )


async def get_clear_order(
    state: FSMContext
) -> dict:
    order_data = await state.get_data()
    order_data.pop("current_section")
    order_data.pop("current_price")
    return order_data
