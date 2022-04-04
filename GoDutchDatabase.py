import mysql.connector
import logging
# TODO: Replace query strings with stored procedures.
# TODO: Replace print calls with something more professional-looking.
class GoDutchDatabase:
    def __init__(self, config: dict):
        self.connection = None
        self.db_usr = config['db_usr']
        self.db_pwd = config['db_pwd']
        self.db_name = config['db_name']
        self.host_name = config['host_name']
        self.__setup()

    def __connect_db(self):
        print(f"Connecting to database '{self.db_name}'...")
        self.connection = mysql.connector.connect(
            host=self.host_name,
            user=self.db_usr,
            password=self.db_pwd,
            database=self.db_name
        )
        print(f"Connected to database '{self.db_name}'.")

    def __connect_server(self):
        print("Connecting to MySQL server...")
        self.connection = mysql.connector.connect(
            host=self.host_name,
            user=self.db_usr,
            password=self.db_pwd
        )
        print("Connected to MySQL server.")

    def __create_db(self):
        print(f"Creating database '{self.db_name}'...")
        query = "CREATE DATABASE db_name WHERE db_name = '%s'"
        cursor = self.connection.cursor()
        cursor.execute(query, (self.db_name,))
        print(f"Database {self.db_name} created.")

    def __drop_db(self):
        print(f"Dropping database '{self.db_name}'")
        query = "DROP DATABASE db_name WHERE db_name = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (self.db_name,))
        print(f"Database '{self.db_name} dropped.'")

    def __setup(self):
        self.__connect_server()
        if not self.__database_exists():
            print(f"Database '{self.db_name}' doesn't exist.")
            self.__create_db()
        self.__connect_db()
        if not self.__table_exists("bot_users"):
            print("Table 'bot_a' doesn't exist.")
            self.__create_user_data_table()
        if not self.__table_exists("transactions"):
            print("Table 'transactions' doesn't exist.")
            self.__create_transaction_data_table()
        print("Setup complete.")

    def __database_exists(self):
        query = """
        SELECT schema_name from INFORMATION_SCHEMA.SCHEMATA WHERE schema_name = %s
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (self.db_name,))
        return cursor.fetchone() is not None

    def __table_exists(self, name: str):
        query = """
        SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_name = %s        
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (name,))
        return cursor.fetchone() is not None

    def __create_transaction_data_table(self):
        print("Creating table 'transactions'...")
        query = """
        CREATE TABLE transactions(
            id INT NOT NULL AUTO_INCREMENT,
            user_id INT NOT NULL,
            transaction_amount FLOAT NOT NULL,
            transaction_name VARCHAR(40) NOT NULL,
            transaction_date DATETIME NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (user_id) REFERENCES bot_users(user_id)
        )
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        print("Table 'transactions' created.")

    def __create_user_data_table(self):
        print("Creating table 'bot_users'...")
        query = """
        CREATE TABLE bot_users (
            id INT NOT NULL AUTO_INCREMENT,
            user_id INT NOT NULL UNIQUE,
            username VARCHAR(40) NOT NULL,
            date_added DATE NOT NULL,
            PRIMARY KEY (id)
        )
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        print("Table 'bot_users' created.")

    def get_user_ids(self):
        query = "SELECT user_id FROM bot_users"
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_user_monthly_total(self, user_id: str, month, year):
        query = """
        SELECT * from transactions WHERE user_id = %s AND month(date) = %s AND year(date) = %s
        """
        if self.user_exists(user_id):
            cursor = self.connection.cursor()
            cursor.execute(query, (user_id, month, year))
        else:
            return None

    def user_exists(self, user_id):
        query = "SELECT 1 from bot_users WHERE user_id=%s"
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchone() is not None

    def add_user(self, user_id, date_added):
        query = "INSERT INTO bot_users (user_id, date_added) VALUES (%s, %s)"
        if not self.user_exists(user_id):
            cursor = self.connection.cursor()
            cursor.execute(query, (user_id, date_added))
            self.connection.commit()

    def add_transaction(self, user_id, transaction_amount, transaction_name, transaction_date):
        if not self.user_exists(user_id):
            self.add_user(user_id, transaction_date)
        query = """
        INSERT INTO transactions (user_id, transaction_amount, transaction_name, transaction_date) 
        VALUES (%s, %s, %s, %s)
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id, transaction_amount, transaction_name, transaction_date))
        self.connection.commit()

    def get_usernames(self):
        query = "SELECT user_id FROM bot_users"
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
