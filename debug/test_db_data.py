import sqlite3

def check_source_chunks_in_db():
    connection = sqlite3.connect("chunk_db/document_chunks.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT chunk_src, COUNT(chunk) FROM document_chunks GROUP BY chunk_src;
        """
    )

    rows = cursor.fetchall()
    connection.close()

    return rows

q = check_source_chunks_in_db()

for row in q:
    print(row)