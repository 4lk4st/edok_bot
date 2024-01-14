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
)-> None:
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
