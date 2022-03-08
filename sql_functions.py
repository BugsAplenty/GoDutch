import mysql.connector
from mysql.connector import Error
import pandas as pd


def create_server_connection(host_name, user_name, user_password):
    import mysql.connector
    from mysql.connector import Error
    connection = None  # drops previous connection
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        print("MySql Database connection successful.")
    except Error as e:
        print(f"Error: {e}")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()  # cursor inside mysql workbench
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"Error: {e}")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()  # makes sure query is impemented
        print("Query successful")
    except Error as e:
        print(f"Error: {e}")



