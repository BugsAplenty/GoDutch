import sqlite3

class GerkulesFoodDB:
    def __init__(self):
        self.conn = sqlite3.connect('gerkules_users.db', check_same_thread=False)
        print("Opened database successfully.")
        self.cursor = self.conn.cursor()

    def run(self):
        self.cursor.execute("""Create TABLE IF NOT EXISTS food(
                food_name text,
                cal_per_100g real
                )
                """)
        print("Table created.")
        self.conn.commit()


gerkules_food_db = GerkulesFoodDB()