import sqlite3


def write_database(commands: str, date_times: str, hotels: str) -> None:
    with sqlite3.connect('user_data.db') as data_base:
        data = data_base.cursor()
        user = (commands, date_times, hotels)
        data.execute("INSERT INTO users VALUES(?, ?, ?);", user)
