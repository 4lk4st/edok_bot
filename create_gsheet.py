from pprint import pprint

from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'creds.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE)
spreadsheet_id = '17DQRfmDI8Ou-uISBxEj0_fUlF2uv2i_LhJ854_-hVvY'


service = build('sheets', 'v4', credentials=credentials)

# Пример чтения файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:E10',
    majorDimension='ROWS'
).execute()
pprint(values)

# # Пример записи в файл
# values = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {"range": "B3:C4",
#              "majorDimension": "ROWS",
#              "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]},
#             {"range": "D5:E6",
#              "majorDimension": "COLUMNS",
#              "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
# 	]
#     }
# ).execute()