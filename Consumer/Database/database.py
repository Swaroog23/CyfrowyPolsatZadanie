import sqlite3
from consts import DATABASE_URI
from typing import Any


def create_database_and_tables_if_not_exists() -> None:
    with sqlite3.connect(DATABASE_URI) as sql_conn:
        cursor = sql_conn.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS key_values (
                    id INTEGER PRIMARY KEY,
                    key INTEGER UNIQUE NOT NULL,
                    value TEXT NOT NULL
                )
                """
        )


def insert_data_to_db(key: str, value: Any) -> None:
    with sqlite3.connect(DATABASE_URI) as sql_conn:
        cursor = sql_conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO key_values (key, value) VALUES (:key, :value)",
                {"key": key, "value": str(value)},
            )
            return None
        except sqlite3.IntegrityError as error:
            return error
        except sqlite3.OperationalError:
            create_database_and_tables_if_not_exists()
            insert_data_to_db(key, value)


def get_data_from_db(key: str) -> Any:
    with sqlite3.connect(DATABASE_URI) as sql_conn:
        cursor = sql_conn.cursor()
        cursor.execute("SELECT value FROM key_values WHERE key=:key", {"key": key})
        return cursor.fetchone()
