import sqlite3


def create_database() -> None:
    """Функция создает базу данных"""
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


def write_database(commands: str, date, times: str, hotels: str) -> None:
    """
    Функция записывает в базу данных
    :param commands: название команды
    :param date: дата создания запроса
    :param times: время создания запроса
    :param hotels: отели, которые получили из запроса
    """
    with sqlite3.connect('user_data.db') as data_base:
        data = data_base.cursor()
        user = (commands, date, times, hotels)
        data.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)


def get_from_db(date_start, date_finish) -> list:
    """
    Функция возвращает из базы данных историю запросов
    по датам.
    """
    with sqlite3.connect('user_data.db') as data_base:
        data = data_base.cursor()
        both_date = (date_start, date_finish)
        data.execute("SELECT * FROM `users` WHERE (`date` > ?) AND (`date` < ?);", both_date)
        all_results = data.fetchall()
        return all_results
