from sql_functions import *
from datetime import datetime


def read_queries_file(path="./MySQL/queries.txt"):
    print(f"Reading queries from path '{path}'")
    queries = []
    with open(path, 'r', encoding='utf-8') as f:
        for lines in f:
            line = lines.strip('\n')
            if line:
                queries.append(line + " ")
    return queries


def index_queries(queries):
    print("Indexing queries")
    queries_dictionary = { }
    for elem in queries:
        queries_dictionary[elem[0]] = elem[1]

    return queries_dictionary


def merge_queries(queries):
    query_list = []
    query, query_name = "", ""
    for elem in queries:
        if elem[0] == "@":
            query = ""
            query_name = elem.strip("@ ")
        else:
            query += elem
            if ";" in elem:
                query_list.append((query_name, query))

    return query_list


def validate_query_file_integrity(path="./MySQL/queries.txt"):
    pass


def create_query_dictionary():
    validate_query_file_integrity()

    queries_raw = read_queries_file()
    queries_combined = merge_queries(queries_raw)
    queries = index_queries(queries_combined)
    return queries


def create_default_database(q, populate=False):
    """creates database with tables, if populate is True then sample data will be added"""

    connection = create_server_connection("localhost", "root", "password")
    execute_query(connection, q["create_database"], "create_database")
    connection = create_db_connection("localhost", "root", "password", "telegrambot")
    execute_query(connection, q["create_user_table"], "create_user_table")
    execute_query(connection, q["create_transactions_table"], "create_transactions_table")
    if populate:
        execute_query(connection, q["populate_sample_data_users"], "populate_sample_data_users")
        execute_query(connection, q["populate_sample_data_transactions"], "populate_sample_data_transactions")


def drop_database(q):
    connection = create_server_connection("localhost", "root", "password")
    execute_query(connection, q["drop_database"], "drop_database")


def user_exists(connection, unique):
    print("Checking if user exists.")
    query = f"SELECT users.fullname FROM users WHERE unique_identifier = '{unique}';"
    result = read_query(connection, query)
    if result:
        return True

    return False


def get_dic_and_db_connection():
    q = create_query_dictionary()
    connection = create_db_connection("localhost", "root", "password", "telegrambot")
    return connection, q


def print_user_doesnt_exist():
    print(f"User doesn't exist.")


def get_today_date():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    return date


def add_user_unique_identifier(connection, q, fullname, unique):
    if user_exists(connection, unique):
        print(f"User {fullname} already exists! - unique identifier: {unique}")
        return None

    date = get_today_date()
    query = q["add_user"].format(fullname=fullname, date=date, unique=unique)
    success = execute_query(connection, query, "add_new_user")
    if success == 1:
        print(f"User {fullname} was added!")
        return 1
    return -1


def get_user_transactions(connection, q, unique):
    if not user_exists(connection, unique):
        print_user_doesnt_exist()
        return None

    query = q["get_users_transactions"].format(unique=unique)
    results = read_query(connection, query)
    return results


def get_user_sum(connection, q, unique):
    """returns a decimal number"""

    if not user_exists(connection, unique):
        print_user_doesnt_exist()
        return None

    print("Getting the sum of all user's transactions")
    query = q["get_user_sum"].format(unique=unique)
    results = read_query(connection, query)
    return results[0][0]


def get_user_transactions_month(connection, q, unique, date="this_month"):
    """gets a user's transaction starting certain month
       takes time in format 'YYYY-MM-DD hh:mm:ss'
       default behavior: returns this month's transactions
    """

    if not user_exists(connection, unique):
        print_user_doesnt_exist()
        return None

    if date == "this_month":
        now = datetime.now()
        date = now.strftime("%Y-%m-1 00:00:00")

    query = q["get_users_transactions_date"].format(unique=unique, date=date)
    results = read_query(connection, query)
    return results


def get_user_transactions_sum_month(connection, q, unique, date="this_month"):
    """gets a user's sum of transaction starting certain month
       takes time in format 'YYYY-MM-DD hh:mm:ss'
       default behavior: returns this month's sum of transactions
    """

    if not user_exists(connection, unique):
        print_user_doesnt_exist()
        return None

    if date == "this_month":
        now = datetime.now()
        date = now.strftime("%Y-%m-1 00:00:00")

    query = q["get_users_transactions_sum_date"].format(unique=unique, date=date)
    results = read_query(connection, query)
    return results[0][0]


def add_transaction(connection, q, unique, fullname, amount):
    if not user_exists(connection, unique):
        print_user_doesnt_exist()
        print("Creating user.")
        add_user_unique_identifier(connection, q, fullname, unique)
        return None

    print("Adding transaction.")

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    query = q["get_id_by_unique_identifier"].format(unique=unique)
    user_id = read_query(connection, query)[0][0]

    query = q["add_transaction"].format(user_id=user_id, amount=amount, date=timestamp)
    success = execute_query(connection, query, "add_transaction")
    if success == 1:
        print(f"Transaction for {fullname} at {amount} was added!")
        return 1
    return -1

