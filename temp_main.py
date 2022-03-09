'''TESTING ENVIRONMENT'''

from sql_functions import *
from backend import *

def temp():
    q = temp_get_queries()
    print(q)
    print("--=-=-=-=-=-=-=---")
    connection = create_server_connection("localhost", "root", "1z2w3c4r")
    execute_query(connection, q["create_database"])
    connection = create_db_connection("localhost", "root", "1z2w3c4r", "telegrambot")
    execute_query(connection, q["create_user_table"])
    execute_query(connection, q["create_transactions_table"])
