from chromadb import PersistentClient
from collections import defaultdict

# like in ingestion we can query chromadb directly and it will embed our query text automatically using all-MiniLM

def cosine_search(query: str, k: int):
    client = PersistentClient(path="chroma_db")
    collection = client.get_collection("qna_data")

    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["metadatas", "documents", "distances"]
    )

    return results

def filter_results_by_threshold(results, threshold:float=0.6):

    filtered_results = defaultdict(list)

    # why distances[0] , docs[0] ?? "results" object has keys documents, distances, etc they are 2D arrays and we really only need the 0th el
    ### so its like {ids: [['5004'...]], documents: [['Osha is the occu..., ]], distances: [[0.05323, ...]]}

    for i, dist in enumerate(results["distances"][0]):
        if dist <= threshold:
            filtered_results["documents"].append(results["documents"][0][i])
            filtered_results["metadatas"].append(results["metadatas"][0][i])
            filtered_results["distance"].append(dist)

    return filtered_results

if __name__ == '__main__':
    res = cosine_search(query="What is OSHA?", k=5)
    print(res)