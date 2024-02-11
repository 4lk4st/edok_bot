from datetime import date, datetime, timedelta
import json

from aiogram import types
from aiogram.fsm.context import FSMContext

from googleapiclient.discovery import build
from google.oauth2 import service_account

from handlers.services import get_clear_order
from keyboards.dao import get_food_price


SERVICE_ACCOUNT_FILE = 'creds.json'
SPREADSHEET_ID = '17DQRfmDI8Ou-uISBxEj0_fUlF2uv2i_LhJ854_-hVvY'


async def write_to_gsheet(
    message: types.Message,
    state: FSMContext
) -> None:
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE)
    service = build('sheets', 'v4', credentials=credentials)

    current_date = str(date.today())
    current_tomsk_time = datetime.utcnow() + timedelta(hours=7)
    current_time_in_str = current_tomsk_time.strftime("%H:%M")

    order_data = await get_clear_order(state)

    user_name = f"{message.from_user.last_name} {message.from_user.first_name}"
    
    for section in order_data.keys():
        for food in order_data[section]:
          
            food_price = get_food_price(section, food.capitalize())
            quantity = order_data[section][food]
            food_cost = food_price * quantity

            service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range="Главная!B:H",
                valueInputOption="USER_ENTERED",
                body={
                    "majorDimension": "ROWS",
                    "values": [
                        [f"{current_date}",
                        f"{current_time_in_str}",
                        f"{user_name}",
                        f"{section}",
                        f"{food}",
                        f"{quantity}",
                        f"{food_price}",
                        f"{food_cost}",
                        ],
                    ]
                }
                ).execute()
    