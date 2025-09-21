from utils.get_sqlite_connection import get_conn_and_cursor
from typing import Tuple
from utils.download_source_data import load_data_source
from chromadb import PersistentClient
from tqdm import tqdm

# NOTE : since we're using chromadb and it uses all-MiniLM-L6-v2 as the default embedding model
# we don't need sentence-transformers and its dependencies.

DB_PATH = "chunk_db/document_chunks.db"
SOURCES = load_data_source()
    
def load_chunks_from_db():
    """Fetch all chunk rows from Chunk DB"""
    try:
        conn, cur = get_conn_and_cursor(DB_PATH)
        cur.execute("SELECT chunk_id, chunk_src, chunk FROM document_chunks;")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Encountered an issue loading chunks from {DB_PATH} : {e}")
        return []
    
def create_metadata(chunk_id: int, source_id: str):
    """Create a metadata object for a source ID (as structured in the sources file)"""

    # group sources by src_id for efficiency, now we dont have to loop and check
    source_grouped = {src["id"]: src for src in SOURCES}
    source_info = source_grouped.get(source_id, {})
    return {
        "chunk_id" : chunk_id,
        "source_id" : source_id,
        "title" : source_info.get("title", f"Unknown source {source_id}"),
        "url" : source_info.get("url", "")
    }


def encode_and_add_to_chroma(rows: Tuple[int, str, str]):
    """We use ChromaDB to embed the chunk rows and add them to a persistent DB on disk."""
    VECTOR_DB_PATH = "chroma_db"
    docs, metas, ids = [], [], []
    chroma_client = PersistentClient(path=VECTOR_DB_PATH)

    for chunk_id, chunk_src, chunk in rows:
        docs.append(chunk)
        metas.append(create_metadata(chunk_id, chunk_src))
        ids.append(str(chunk_id))

    # in case of default embedding, we dont need to provide it anything for embedding_function
    try:
        vector_store = chroma_client.create_collection("qna_data")
        # we couldn't see any progress + dataset is large so batching is a good fix

        for i in tqdm(range(0, len(docs), 200), desc="Adding docs to ChromaDB"):
            batch_ids, batch_metas, batch_docs = ids[i:i+200], metas[i:i+200], docs[i:i+200]
            vector_store.add(
            ids= batch_ids,
            documents= batch_docs,
            metadatas=batch_metas
            )

        print(f"Embedded and added {len(docs)} documents to ChromaDB and saved at {VECTOR_DB_PATH}")
    except Exception as e:
        print(f"Encountered an issue while embedding and ingesting docs : {e}")

if __name__ == '__main__':
    rows = load_chunks_from_db()
    encode_and_add_to_chroma(rows)