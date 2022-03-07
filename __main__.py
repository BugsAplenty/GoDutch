#!/usr/bin/python3
from pyrogram import Client
from databases.user_database import gerkules_user_db

app = Client("gerkules", config_file="gerkules.ini")

# App launch
if __name__ == "__main__":
    gerkules_user_db.run()
    app.run()
