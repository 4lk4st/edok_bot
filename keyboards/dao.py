from datetime import datetime

from .data import menu


NUMBER_DAY = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

today_number = datetime.weekday(datetime.today())
today_str = NUMBER_DAY[today_number]

def get_menu_sections() -> list[str]:
    menu_sections = list(menu[today_str].keys())

    return menu_sections

def get_food_list(section:str) -> list[str]:
    food_list = list(menu[today_str][section].keys())

    return food_list