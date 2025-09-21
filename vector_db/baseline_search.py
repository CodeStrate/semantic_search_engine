from chromadb import PersistentClient
from collections import defaultdict

# like in ingestion we can query chromadb directly and it will embed our query text automatically using all-MiniLM

def cosine_search(query: str, k: int, threshold: float = 0.6):
    client = PersistentClient(path="chroma_db")
    collection = client.get_collection("qna_data")

    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["metadatas", "documents", "distances"]
    )

    filtered_results_by_thresh = defaultdict(list)

    for i, dist in enumerate(results["distances"][0]):
        if dist <= threshold:
            filtered_results_by_thresh["documents"].append(results["documents"][0][i])
            filtered_results_by_thresh["metadatas"].append(results["metadatas"][0][i])
            filtered_results_by_thresh["distance"].append(dist)

    return filtered_results_by_thresh

if __name__ == '__main__':
    res = cosine_search(query="What is OSHA?", k=5)
    for r in res['documents']:
        print(r)