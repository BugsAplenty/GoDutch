import gspread
from oauth2client.service_account import ServiceAccountCredentials

gc = gspread.service_account(filename='./client_secret.json')
sh = gc.open("Calorie Database")
print(sh.sheet1.get('A1'))
