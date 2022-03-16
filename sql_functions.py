import mysql.connector
from mysql.connector import Error


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(f"MySQL Database connection successful - {db_name}")
    except Error as err:
        print(f"Error: '{err}'")
        return -1

    return connection


def create_server_connection(host_name="localhost", user_name="root", user_password="password"):
    import mysql.connector
    from mysql.connector import Error
    connection = None  # drops previous connection
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        print(f"MySql Database connection successful - {host_name}")
    except Error as err:
        print(f"Error: {err}")
        return -1

    return connection


def create_database(connection, query):
    cursor = connection.cursor()  # cursor inside mysql workbench
    try:
        cursor.execute(query)
        print("Database created successfully")
        return 1
    except Error as e:
        print(f"Error: {e}")
        return -1


def execute_query(connection, query, query_name="unnamed"):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print(f"Query successful - {query_name}")
        return 1
    except Error as e:
        print(f"Error: {e}")
        return -1


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: {e}")
        return -1

