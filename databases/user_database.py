import sqlite3
from sqlite3 import Error


class GerkulesUserDB:
    def __init__(self):
        self.conn = sqlite3.connect('gerkules_users.db', check_same_thread=False)
        print("Opened database successfully.")
        self.cursor = self.conn.cursor()

    def run(self):
        self.cursor.execute("""Create TABLE IF NOT EXISTS users(
                username text,
                stage integer,
                quota real
                )
                """)
        print("Table created.")
        self.conn.commit()


gerkules_user_db = GerkulesUserDB()
