from bm25s import tokenize, BM25
from vector_db.baseline_search import cosine_search
import numpy as np
import random
from utils.normalize_scores import normalize_scores

random.seed(42) # seed to force deterministic answers from reranking

def hybrid_reranking(query:str, k:int=30, alpha:float=0.6):
    res = cosine_search(query, k)
    docs, metas, distances = res['documents'][0], res['metadatas'][0], res['distances'][0]
    # 1. we need scores and normalized (0-1) current distance is closer/lower = better , scores are higher = better so we flip 1 - dist
    vec_scores = 1 - np.array(distances)
    vec_scores_norm = normalize_scores(vec_scores)

    # this uses the same method as scikit learn's Count Vectorizer, and this BM25 lib uses scipy under the hood
    tokenized_docs = tokenize(docs)
    reranker = BM25()
    reranker.index(tokenized_docs)
    query_tokens = tokenize(query)

    reranker_scores = reranker.retrieve(query_tokens, k=len(docs)).scores[0]
    reranker_scores_norm = normalize_scores(reranker_scores)

    # blend scores
    blended_scores = alpha * vec_scores_norm + (1 - alpha) * reranker_scores_norm


    # sort 
    reranked_results = sorted(
        zip(docs, metas, blended_scores),
        key= lambda x: x[2],
        reverse=True
    )

    return reranked_results

if __name__ == '__main__':
    res = hybrid_reranking(query="What is OSHA?")
    print(res)


