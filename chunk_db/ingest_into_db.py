import sqlite3, os
from utils.common_utils import get_conn_and_cursor, load_data_source
from tqdm import tqdm
from chunk_db.chunk_data import load_data, chunk_data

sources = load_data_source()


DB_PATH = "chunk_db/document_chunks.db"
DATA_PATH = "sourced_data"

def create_table():
    """Create the Table/Schema to store chunks in SQLite"""
    try:
        connection, cursor = get_conn_and_cursor(DB_PATH)
        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_chunks (
        chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk_src TEXT,
        chunk TEXT
        );
        """
        )

        connection.commit()
        print(f"Table was created at {DB_PATH}")
    except Exception as e:
        print(f"There was an issue creating the SQLite database/table : {e}")

def ingest_chunks():
    """Load each PDF and chunk and ingest it into the created DB/Table."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for source in tqdm(sources, desc="Loading documents from source.."):
        src_id = source["id"]
        file_path = os.path.join(DATA_PATH, f"{src_id}.pdf")

        if not os.path.exists(file_path):
            print(f"{src_id} data file is missing. Moving on..")
            continue

        print(f"Processing {file_path} for chunking and ingestion..")

        try:
            doc = load_data(file_path)
            chunks = chunk_data(doc, separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ": ", "•","• ", " - ", ", "])

            for chunk in chunks:
                cursor.execute(
                    """
                    INSERT INTO document_chunks (chunk_src, chunk) VALUES (?, ?)
                    """,
                    (src_id, chunk)
                )
            print(f"Stored {len(chunks)} chunks for {file_path}")
        except Exception as e:
            print(f"Encountered an issue while ingesting {file_path} : {e}")

    connection.commit()
    connection.close()
    print(f"All data was chunked and stored in {DB_PATH}")

if __name__ == '__main__':
    create_table()
    ingest_chunks()
