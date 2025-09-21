import sqlite3

def get_conn_and_cursor(db_path:str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    return connection, cursor