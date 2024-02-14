from datetime import datetime, timedelta

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

def get_today_number() -> int:
    today_number = datetime.weekday(datetime.today())

    # блок для сравнения текущего времени со временем смены меню: 09:45 текущего дня
    # переписать позже в отдельную функцию, с константами из .env файла
    current_tomsk_time = datetime.utcnow() + timedelta(hours=7)
    hours_minutes = current_tomsk_time.strftime("%H:%M")
    hours, minutes = map(int, hours_minutes.split(':'))
    current_time_one_int = hours + (minutes / 60)

    time_x = 9 + (45 / 60)

    if current_time_one_int > time_x:
        today_number += 1

    return today_number


today_str = NUMBER_DAY[get_today_number()] if get_today_number() in range(5) else "Понедельник"

def get_menu_sections() -> list[str]:
    menu_sections = list(menu[today_str].keys())

    return menu_sections

def get_food_list(section:str) -> list[str]:
    food_list = list(menu[today_str][section].keys())

    return food_list

def get_all_food() -> list[str]:
    all_food_list:list = []
    for section in get_menu_sections():
        for food in get_food_list(section):
            all_food_list.append(food)

    return all_food_list

def get_food_price(section:str, food:str) -> int:  
    return menu[today_str][section][food]["цена"]
