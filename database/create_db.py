import sqlite3


def create_database() -> None:
    with sqlite3.connect('user_data.db') as data_base:
        data = data_base.cursor()
        data.execute(
            """CREATE TABLE IF NOT EXISTS users (
                command TEXT,
                date DATE,
                time TEXT,
                hostels TEXT
            )
        """)
