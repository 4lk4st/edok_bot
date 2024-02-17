from datetime import datetime, timedelta

from .data import menu


SHIFTING_TIME = "09:45"


def convert_hm_to_int(time_str:str) -> int:
    '''
    Переводит время в строковом формате "HH:MM" в число, где:
    целая часть - количество часов,
    дробная часть - количество минут, деленное на 60 (доля от часа)
    '''
    hours, minutes = map(int, time_str.split(':'))
    time_int = hours + (minutes / 60)

    return time_int  

def get_next_menu_day(menu: dict) -> str:
    '''
    Определяет первый будущий день, который есть в меню,
    и возвращает его дату в формате "ГГГГ-ММ-ДД"
    '''
    for day in menu.keys():
        if day > datetime.today().strftime("%Y-%m-%d"):
            return day
    # если следующего дня в меню нет - вернуть "заглушку"
    return "Меню не загружено"

def get_order_date(shifting_time:str, menu:dict) -> str:
    '''
    Выдает день, на который нужно показать меню пользователю.
    Выбор дня зависит от наличия меню "на сегодня"
    и времени дня относительно константы TIME_SHIFT.
    '''
    current_tomsk_time = datetime.today()
    current_day_str = current_tomsk_time.strftime("%Y-%m-%d")
    current_time_str = current_tomsk_time.strftime("%H:%M")

    current_time = convert_hm_to_int(current_time_str)
    shift_time = convert_hm_to_int(shifting_time)

    if current_day_str in menu and current_time < shift_time:
        return current_day_str
    else:
        return get_next_menu_day(menu)

def get_current_menu(order_date: str) -> dict:
    '''
    Даёт меню на тот день, который надо показать сейчас пользователю,
    в виде словаря с вложенностью "Категория - Блюдо - Цена".
    Если меню не загружено - выдает заглушку, чтобы бот не падал.
    '''
    if order_date == "Меню не загружено":
            return {"Меню не загружено!":
                    {"Сообщите администратору!":
                        {"цена": 0}}}
    
    return menu[order_date]

def get_menu_sections() -> list[str]:
    menu_sections = list(get_current_menu(
        get_order_date(SHIFTING_TIME, menu))
        )

    return menu_sections

def get_food_list(section:str) -> list[str]:
    food_list = list(get_current_menu(
        get_order_date(SHIFTING_TIME, menu))[section].keys())

    return food_list

def get_all_food() -> list[str]:
    all_food_list:list = []
    for section in get_menu_sections():
        for food in get_food_list(section):
            all_food_list.append(food)

    return all_food_list

def get_food_price(section:str, food:str) -> int:  
    return get_current_menu(
        get_order_date(SHIFTING_TIME, menu))[section][food]["цена"]
