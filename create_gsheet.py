from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'creds.json'
SPREADSHEET_ID = '17DQRfmDI8Ou-uISBxEj0_fUlF2uv2i_LhJ854_-hVvY'


def write_to_gsheet(
    current_date:str,
    current_tomsk_time:str,
    user_name:str,
    order_str:str
) -> None:
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE)
    service = build('sheets', 'v4', credentials=credentials)

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!B:E",
        valueInputOption="USER_ENTERED",
        body={
            "majorDimension": "ROWS",
            "values": [
                [f"{current_date}", f"{current_tomsk_time}", f"{user_name}", f"{order_str}"],
            ]
        }
        ).execute()
    