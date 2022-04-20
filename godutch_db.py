import datetime

import mysql.connector
from typing import Tuple


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


def get_all_user_ids(connection: mysql.connector.MySQLConnection) -> Tuple[int]:
    cursor = connection.cursor()
    cursor.callproc("get_all_user_ids")
    user_ids = result2tuple(cursor)
    return user_ids


def result2tuple(cursor) -> tuple:
    results = []
    for result in cursor.stored_results():
        results.extend(result.fetchall())
    return tuple(result[0] for result in results)


def get_all_monthly_totals(connection: mysql.connector.MySQLConnection, month: int, year: int) -> list:
    results = []
    cursor = connection.cursor()
    date = datetime.datetime(year, month, 1)
    cursor.callproc("get_all_monthly_totals", [date, ])
    for result in cursor.stored_results():
        results.extend(result.fetchall())
    return results


def get_user_monthly_total(connection: mysql.connector.MySQLConnection,
                           user_id: int,
                           month: int,
                           year: int) -> (int, int):
    cursor = connection.cursor()
    date = datetime.datetime(year, month, 1)
    cursor.callproc("get_user_monthly_total", [user_id, date])
    totals = result2tuple(cursor)
    return totals[0]


def get_username_by_id(connection: mysql.connector.MySQLConnection, user_id: int) -> str:
    cursor = connection.cursor()
    cursor.callproc("get_username_by_id", [user_id, ])
    usernames = result2tuple(cursor)
    return usernames[0]


def user_exists(connection: mysql.connector.MySQLConnection, user_id: int):
    cursor = connection.cursor()
    cursor.callproc("user_exists", [user_id, ])
    bool_user_exists = result2tuple(cursor)
    return bool_user_exists


def add_user(connection: mysql.connector.MySQLConnection, user_id, username, date_added):
    cursor = connection.cursor()
    cursor.callproc("add_user", [user_id, username, date_added])
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
