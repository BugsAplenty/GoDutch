from sql_functions import *
from backend import *


# requires PyTest package
# run "pytest unit_testing.py" in terminal to run all tests in this file
# all test functions must start with "test_", eg: "test_foo"


def test_sql_connect():
    assert str(type(create_server_connection("localhost", "root", "password"))) == "<class 'mysql.connector.connection_cext.CMySQLConnection'>"
    assert create_server_connection("localhost", "root", "mock_password") == -1


def test_sql_connect_db():
    assert str(type(create_db_connection("localhost", "root",
                                             "password", "telegrambot"))) == "<class 'mysql.connector.connection_cext.CMySQLConnection'>"
    assert create_db_connection("localhost", "root",
                                             "password", "mock_database") == -1


def test_create_database():
    pass


def test_sql_execute_query():
    pass


def test_sql_read_query():
    pass