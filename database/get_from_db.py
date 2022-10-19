import sqlite3


def get_from_db(date_start, date_finish):
    with sqlite3.connect('user_data.db') as data_base:
        data = data_base.cursor()
        both_date = (date_start, date_finish)
        data.execute("SELECT * FROM `users` WHERE (`date` > ?) AND (`date` < ?);", both_date)
        all_results = data.fetchall()
        return all_results
