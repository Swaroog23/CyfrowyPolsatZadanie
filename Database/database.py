import sqlite3


def create_database_and_tables():
    with sqlite3.connect('key_value.db') as sql_conn:
        with sql_conn.cursor() as cursor:
            try:
                cursor.execute("""
                            CREATE TABLE key_values (
                                key INTEGER,
                                value TEXT
                            )
                            """)
            except sqlite3.OperationalError:
                pass


def insert_data_to_db(key, value):
    with sqlite3.connect('key_value.db') as sql_conn:
        with sql_conn.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO key_values VALUES (:key, :value)",
                               {'key': key, 'value': value})
                return 1
            except sqlite3.OperationalError:
                return 0


def get_data_from_db(key):
    with sqlite3.connect('key_value.db') as sql_conn:
        with sql_conn.cursor() as cursor:
            try:
                cursor.execute("SELECT key, value FROM key_values WHERE key=:key",
                               {'key': key})
                return cursor.fetchone()
            except sqlite3.OperationalError:
                return 0
