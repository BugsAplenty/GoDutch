import mysql.connector


def connect_db(db_config):
    print(f"Connecting to database '{db_config['db_name']}'...")
    connection = mysql.connector.connect(
        host=db_config['host_name'],
        user=db_config['db_usr'],
        password=db_config['db_pwd'],
        database=db_config['db_name']
    )
    print(f"Connected to database '{db_config['db_name']}'.")
    return connection


def get_all_user_ids(connection: mysql.connector.MySQLConnection):
    cursor = connection.cursor()
    cursor.callproc("get_all_user_ids")
    for result in cursor.stored_results():
        return result.fetchall()


def get_all_usernames(connection: mysql.connector.MySQLConnection):
    cursor = connection.cursor()
    cursor.callproc("get_all_usernames")
    for result in cursor.stored_results():
        return result.fetchall()


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


def add_user(connection: mysql.connector.MySQLConnection, user_id, date_added):
    if not user_exists(connection, user_id):
        cursor = connection.cursor()
        cursor.callproc("add_user", [user_id, date_added])
        connection.commit()

def update_username(connection: mysql.connector.MySQLConnection, user_id, username):
    if user_exists(connection, user_id):
        curr_username = get_username_by_id(connection, user_id)
        if curr_username != username:
            cursor = connection.cursor()
            cursor.callproc("modify_username", [user_id, username])
            connection.commit()


def add_transaction(connection: mysql.connector.MySQLConnection,
                    user_id,
                    transaction_amount,
                    transaction_name,
                    transaction_date):
    if user_exists(connection, user_id):
        cursor = connection.cursor()
        cursor.callproc("add_transaction", [user_id, transaction_amount, transaction_name, transaction_date])
        connection.commit()
