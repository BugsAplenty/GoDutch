import mysql.connector


def connect_db(db_config):
    print(f"Connecting to database '{self.db_name}'...")
    connection = mysql.connector.connect(
        host=db_config['host_name'],
        user=db_config['db_usr'],
        password=db_config['db_pwd'],
        database=db_config['db_name']
    )
    print(f"Connected to database '{db_config['db_name']}'.")
    return connection


def get_user_monthly_total(connection: mysql.connector.MySQLConnection, user_id: int, month: int, year: int):
    cursor = connection.cursor()
    cursor.callproc("get_user_monthly_total", [user_id, month, year])
    for result in cursor.stored_results():
        return result.fetchall()


def get_username_by_id(connection: mysql.connector.MySQLConnection, user_id: int):
    cursor = connection.cursor()
    cursor.callproc("get_username_by_id", [user_id, ])
    for result in cursor.stored_results():
        return result.fetchall()


def user_exists(connection: mysql.connector.MySQLConnection, user_id: int):
    cursor = connection.cursor()
    cursor.callproc("user_exists", [user_id, ])
    for result in cursor.stored_results():
        return result.fetchall()


def add_user(self, user_id, date_added):
    query = "INSERT INTO bot_users (user_id, date_added) VALUES (%s, %s)"
    if not self.user_exists(user_id):
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id, date_added))
        self.connection.commit()


def add_transaction(self, user_id, transaction_amount, transaction_name, transaction_date):
    if not self.user_exists(user_id):
        self.add_user(user_id, transaction_date)
    query = """
    INSERT INTO transactions (user_id, transaction_amount, transaction_name, transaction_date) 
    VALUES (%s, %s, %s, %s)
    """
    cursor = self.connection.cursor()
    cursor.execute(query, (user_id, transaction_amount, transaction_name, transaction_date))
    self.connection.commit()


def update_username(user_id: int, username: str):
    pass
