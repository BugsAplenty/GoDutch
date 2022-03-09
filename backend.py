



'''def read_queries_file(path="./MySQL/queries.txt"):
    queries = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        if line:
            queries.append(line)
    return queries

def index_queries():
    pass


def merge_queries(queries):
    query_list = []
    return query_list


def create_query_dictionary():
    queries = read_queries_file()
    queries = merge_queries(queries)
    pass'''



def temp_get_queries():
    # temporary function until
    # make a function that reads queries from txt
    # triple quote for multiline string
    queries = {
        "create_database": "CREATE DATABASE telegrambot;",
        "create_user_table": """ 

    CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    fullname VARCHAR(40) NOT NULL,
    date_created DATE NOT NULL,
    unique_identifier VARCHAR(40) NOT NULL,
    PRIMARY KEY (id)
    );
    """,
        "create_transactions_table": """
        CREATE TABLE transactions(
        id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL,
        transaction_amount int NOT NULL,
        transaction_date DATETIME NOT NULL,
        PRIMARY KEY (id)
        );
        """,

        "select_database": """
        SELECT DATABASE telegrambot;
        """
    }
    return queries
