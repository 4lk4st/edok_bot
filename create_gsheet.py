import pygsheets


client = pygsheets.authorize()
sh = client.open_by_url('https://docs.google.com/spreadsheets/d/17DQRfmDI8Ou-uISBxEj0_fUlF2uv2i_LhJ854_-hVvY/edit?usp=sharing')

wks = sh.sheet1
wks.update_value('A1', "Numbers on Stuff")