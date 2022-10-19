import sqlite3


def write_database(commands: str, date, times: str, hotels: str) -> None:
    with sqlite3.connect('user_data.db') as data_base:
        data = data_base.cursor()
        user = (commands, date, times, hotels)
        data.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
