import json

from datetime import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'creds.json'
SPREADSHEET_ID = '17DQRfmDI8Ou-uISBxEj0_fUlF2uv2i_LhJ854_-hVvY'


def read_from_gsheet() -> dict:
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE)
    service = build('sheets', 'v4', credentials=credentials)

    gsheet_menu = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range="Меню",
                ).execute()
    
    return gsheet_menu['values'][1::]


def create_menu_dict(excel_data:list) -> dict:
    new_menu = {}

    for row in excel_data:
        menu_date:str = datetime.strptime(row[0], "%d.%m.%Y").strftime("%Y-%m-%d")
        menu_category:str = row[1]
        menu_name:str = row[2]
        menu_price:int = row[3]

        if menu_date in new_menu:
            if menu_category in new_menu[menu_date]:
                new_menu[menu_date][menu_category].update(
                    dict([(menu_name,
                        dict([("цена", int(menu_price))]))])
                )
            else:
                new_menu[menu_date].update(
                    dict([(menu_category,
                                    dict([(menu_name,
                                        dict([("цена", int(menu_price))]))]))])
                )
        else:
            new_menu.update(
                {menu_date: dict([(menu_category,
                                    dict([(menu_name,
                                        dict([("цена", int(menu_price))]))]))])}
            )

    return new_menu


def write_to_data_py(menu_dict:dict) -> None:

    with open('keyboards/data.py', 'r+') as f:
        f.truncate(0)
        f.write("menu = ")
        f.write(json.dumps(
            menu_dict,
            sort_keys=False,
            indent=2,
            ensure_ascii=True,
            separators=(',', ': ')
            ))


if __name__ == '__main__':
    write_to_data_py(create_menu_dict(read_from_gsheet()))