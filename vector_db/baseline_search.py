from chromadb import PersistentClient

# like in ingestion we can query chromadb directly and it will embed our query text automatically using all-MiniLM

def cosine_search(query: str, k: int, threshold: float = 0.6):
    client = PersistentClient(path="chroma_db")
    collection = client.get_collection("qna_data")

    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["metadatas", "documents", "distances"]
    )

    return results

if __name__ == '__main__':
    res = cosine_search(query="What are the health hazards of wood dust?", k=3)
    print(res["documents"][0])