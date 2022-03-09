from sql_functions import *


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
    for elem in queries:
        if elem[0] == "@":
            query = ""
            query_name = elem.strip("@ ")
        else:
            query += elem
            if ";" in elem:
                query_list.append((query_name, query))

    return query_list


def create_query_dictionary():
    queries_raw = read_queries_file()
    queries_combined = merge_queries(queries_raw)
    queries = index_queries(queries_combined)
    return queries


def check_query_file_validity():
    pass


def create_default_database(q, populate=False):
    connection = create_server_connection("localhost", "root", "1z2w3c4r")
    execute_query(connection, q["create_database"], "create_database")
    connection = create_db_connection("localhost", "root", "1z2w3c4r", "telegrambot")
    execute_query(connection, q["create_user_table"], "create_user_table")
    execute_query(connection, q["create_transactions_table"], "create_transactions_table")
    if populate:
        execute_query(connection, q["populate_sample_data_users"], "populate_sample_data_users")
        execute_query(connection, q["populate_sample_data_transactions"], "populate_sample_data_transactions")


def drop_database(q):
    connection = create_server_connection("localhost", "root", "1z2w3c4r")
    execute_query(connection, q["drop_database"], "drop_database")


def user_exists(unique):
    connection = create_db_connection("localhost", "root", "1z2w3c4r", 'telegrambot')
    query = f"SELECT users.fullname FROM users WHERE unique_identifier = '{unique}';"
    result = read_query(connection, query)
    if result:
        return True

    return False


def add_user_unique_identifier(fullname, date, unique):
    print("Checking if user already exists.")
    if user_exists(unique):
        print(f"User {fullname} already exists! - unique identifier: {unique}")
        return

    connection = create_db_connection("localhost", "root", "1z2w3c4r", 'telegrambot')
    query = f"INSERT INTO users (fullname, date_created, unique_identifier) VALUES ('{fullname}', '{date}', '{unique}');"
    execute_query(connection, query, "add_new_user")
    print(f"User {fullname} was added!")


def get_user_transactions(unique):
    print("Checking if user exists.")
    if not user_exists(unique):
        print(f"User doesn't exist.")
        return

    connection = create_db_connection("localhost", "root", "1z2w3c4r", 'telegrambot')
    query = f"""
            SELECT users.unique_identifier, transactions.transaction_amount, transactions.transaction_date FROM transactions
            JOIN users ON users.id = transactions.user_id
            HAVING users.unique_identifier = '{unique}'
            ;
    """

    results = read_query(connection, query)
    return results


def get_user_sum(unique):
    print("Checking if user exists.")
    if not user_exists(unique):
        print(f"User doesn't exist.")
        return

    connection = create_db_connection("localhost", "root", "1z2w3c4r", 'telegrambot')
    query = f"""
                SELECT users.unique_identifier, SUM(transactions.transaction_amount) FROM transactions
                JOIN users ON users.id = transactions.user_id
                GROUP BY users.unique_identifier
                HAVING users.unique_identifier = '{unique}'
                ;
            """

    results = read_query(connection, query)
    return results