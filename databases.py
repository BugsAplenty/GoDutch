import gspread
from oauth2client.service_account import ServiceAccountCredentials

gerkules_client = gspread.service_account(filename='./client_secret.json')
databases = gerkules_client.open("Gerkules Databases")

foods = databases.worksheet("Foods")

users = databases.worksheet("Users")
usernames = users.col_values(0)
user_ids = users.col_values(1)

def update_user(user):
    if user['id'] in user_ids and user['username'] in usernames:
        return
    elif user['id'] in user_ids and user['username'] not in usernames:
        cell = users.find(user['id'])
        index = (cell.row, 0)
