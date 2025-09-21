from utils.get_sqlite_connection import get_conn_and_cursor

def check_source_chunks_in_db():
    """Test script/query to check the data was inserted correctly."""
    connection, cursor = get_conn_and_cursor("chunk_db/document_chunks.db")

    # cursor.execute(
    #     """
    #     SELECT chunk_src, COUNT(chunk) FROM document_chunks GROUP BY chunk_src;
    #     """
    # )

    # check quality of chunks
    cursor.execute(
        """
        SELECT chunk_src, chunk from document_chunks ORDER BY RANDOM() LIMIT 2;
        """
    )

    rows = cursor.fetchall()
    connection.close()

    return rows

q = check_source_chunks_in_db()

for row in q:
    print(row)