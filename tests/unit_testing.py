from sql_functions import *
from backend import *


# requires PyTest package
# run "pytest unit_testing.py" in terminal to run all tests in this file
# all test functions must start with "test_", eg: "test_foo"


def get_dictionary_and_server_connection():
    q = create_query_dictionary()
    connection = create_server_connection("localhost", "root", "password")
    return connection, q


def get_dictionary_and_db_connection():
    q = create_query_dictionary()
    connection = create_db_connection("localhost", "root", "password", "mock_telegrambot")
    return connection, q


def test_sql_connect():
    assert str(type(create_server_connection("localhost", "root", "password"))) == "<class 'mysql.connector.connection_cext.CMySQLConnection'>"
    assert create_server_connection("localhost", "root", "mock_password") == -1


def test_sql_connect_db():
    assert str(type(create_db_connection("localhost", "root",
                                             "password", "telegrambot"))) == "<class 'mysql.connector.connection_cext.CMySQLConnection'>"
    assert create_db_connection("localhost", "root",
                                             "password", "mock_database") == -1


def test_create_database():
    connection, q = get_dictionary_and_server_connection()
    assert create_database(connection, q["create_mock_database"]) == 1
    assert create_database(connection, q["nonexistent_query"]) == -1



def test_sql_execute_query():
    connection, q = get_dictionary_and_server_connection()
    assert execute_query(connection, q["drop_mock_database"]) == 1
    assert execute_query(connection, q["nonexistent_query"]) == -1



def test_sql_read_query():
    pass


def test_create_db_for_testing():
    """create a database for upcoming tests"""
    connection, q = get_dictionary_and_server_connection()
    create_database(connection, q["create_mock_database"])
    connection = create_db_connection("localhost", "root", "password", 'mock_telegrambot')
    execute_query(connection, q["create_user_table"])
    execute_query(connection, q["create_transactions_table"])
    execute_query(connection, q["populate_sample_data_users"])
    execute_query(connection, q["populate_sample_data_transactions"])


def test_add_user():
    connection, q = get_dictionary_and_db_connection()
    assert add_user_unique_identifier(connection, q, "not_unique_user", "2011-03-15 10:00:00", "test1") is None
    assert add_user_unique_identifier(connection, q, "invalid_date", "mock_date", "unique_id") == -1
    assert add_user_unique_identifier(connection, q, "proper_user", "2011-03-15 10:00:00", "unique_id") == 1


def test_get_user_transactions():
    connection, q = get_dictionary_and_db_connection()
    assert get_user_transactions(connection, q, "nonexistent_user") is None
    l = get_user_transactions(connection, q, "test3")
    assert type(l) is list
    assert l[0][0] == 100
    assert l[0][2] == 'test3'


def test_get_user_sum():
    connection, q = get_dictionary_and_db_connection()
    assert get_user_sum(connection, q, "nonexistent_user") is None
    assert get_user_sum(connection, q, "test5") == 150


def test_get_user_transactions_month():
    pass


def test_get_user_transactions_sum_month():
    connection, q = get_dictionary_and_db_connection()
    assert get_user_transactions_sum_month(connection, q, "nonexistent_user", date="this_month") is None
    # assert get_user_transactions_sum_month(connection, q, "test1", date="this_month") == 0
    pass


def test_drop_database_and_finish_testing():
    """this marks the end of the unit testing"""
    connection, q = get_dictionary_and_server_connection()
    execute_query(connection, q["drop_mock_database"])



