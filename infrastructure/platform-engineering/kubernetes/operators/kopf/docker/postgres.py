import psycopg2
from faker import Faker
from kubernetes import config

class PostgresClient:
    def __init__(self, host, username, password, db):
        self.host = host
        self.username = username
        self.__password = password
        self.db = db
        self.__connection = None

    def connect_if_not_connected(self):
        if self.__connection is None:
            self.__connection = psycopg2.connect(database=self.db, user=self.username, password=self.__password, host=self.host)

    def get_connection(self):
        return self.__connection
    
    # define other getters/setters accordingly

    def insert_row(self, table, fields):
        self.connect_if_not_connected()
        db_connection = self.get_connection()
        # Idempotent insertions <3
        _fields = ', '.join(fields)
        _values = ', '.join(['%s'] * len(fields))
        
        values = {}
        for elemento in fields:
            values[elemento] = getattr(fake, elemento)()

        insert_query = f"""INSERT INTO {table} ({_fields}) VALUES ({_values})"""

        # RIP exception handling :P
        with db_connection.cursor() as cursor:
            cursor.execute(insert_query, values)
            db_connection.commit()
