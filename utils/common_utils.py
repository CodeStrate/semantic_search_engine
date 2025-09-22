import sqlite3, json

def load_data_source(file_path:str="sources.json"):
    """Load the sources JSON file."""
    with open(file_path, "r", encoding="utf-8") as data_src:
        sources = json.load(data_src)
        return sources

def get_conn_and_cursor(db_path:str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    return connection, cursor