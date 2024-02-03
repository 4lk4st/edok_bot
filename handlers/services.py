import json

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import (as_list, as_marked_section,
                                      Bold, as_key_value, HashTag, Text)


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


async def get_order_info(
    state: FSMContext   
) -> str:
    order_data = await state.get_data()
    order_data.pop("current_section")
    price = order_data.pop("current_price")

    message_text = ""
    
    emoji_for_section = {
        "Салаты": "\U0001F966",
        "Каши": "\U0001F365",
        "Супы": "\U0001F963",
        "Вторые блюда": "\U0001F357",
        "Выпечка": "\U0001F369",
        "Напитки и десерты": "\U0001F378",
    }

    for section, foods in order_data.items():
        if section in emoji_for_section:
            section = f"{emoji_for_section[section]} {section}"
            
        message_text += f"<b>{section}</b>: "
        message_text += "\n"
        for food, quantity in foods.items():
            message_text += f"{food} - {quantity} шт.\n"

    return message_text


async def send_intermediate_order(
    message: types.Message,
    state: FSMContext   
) -> None:

    order_data = await get_order_info(state)
    message_text = "Вы выбрали:\n" + order_data

    await message.answer(message_text)


async def send_final_order(
    message: types.Message,
    state: FSMContext   
) -> None:

    order_data = await get_order_info(state)

    message_text = ("Ваш итоговый заказ:\n\n"
                    + order_data
                    + "\nнаправлен администратору на обработку!")

    await message.answer(
        message_text,
        reply_markup=types.ReplyKeyboardRemove()
    )


async def get_clear_order(
    state: FSMContext
) -> dict:
    order_data = await state.get_data()
    order_data.pop("current_section")
    order_data.pop("current_price")
    return order_data
