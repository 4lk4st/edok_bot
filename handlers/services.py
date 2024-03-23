from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards import get_food_price, get_order_date, SHIFTING_TIME, menu


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

    # если в информации о заказе нет упоминания о данном разделе
    # то создаем и раздел и запись о заказе блюда
    if current_section not in current_order_data:
        await state.update_data(
            {current_section: {f"{food}": 1}}
        )
    # если в информации о заказе уже есть блюдо из данного раздела
    # но не то, которое мы заказываем - записываем в нужный раздел
    elif ((current_section in current_order_data)
        and (food not in current_order_data[current_section])):
        current_order_data[current_section].update({f"{food}": 1})
        await state.set_data(current_order_data)
    # если в информации о заказе уже есть блюдо из данного раздела
    # и мы его уже включили в заказ - добавляем +1 к количеству
    else:
        current_quantity = current_order_data[current_section][food]
        current_order_data[current_section][food] = current_quantity + 1
        await state.set_data(current_order_data)

    current_order_data = await state.get_data()
    current_order_data["current_price"] += get_food_price(current_section, food.capitalize())
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

    message_text += f"<b>Стоимость заказа</b>: {price} руб.\n"
    
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

    message_text = ("Ваш итоговый заказ на "
                    + f"<b>{get_order_date(SHIFTING_TIME, menu)}</b>:\n"
                    + order_data
                    + "\nЗаказ записан на сервере "
                    + "\nи передан Анастасие на формирование \U0001F680."
                    + "\nНе забудьте перевести деньги за еду \U0001F609")

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


async def get_food_quantity(
    state:FSMContext
) -> int:
    order_data = await get_clear_order(state)
    
    food_quantity = 0
    
    for section in order_data.keys():
        for food in order_data[section]:
            food_quantity += 1

    return food_quantity
