import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, status
from api.qna_model import QnAModel
from vector_db.baseline_search import cosine_search, filter_results_by_threshold
from hybrid_reranker.bm25_reranker import hybrid_reranking
from utils.retrieval_utils import query_result_with_citations
import uvicorn

app = FastAPI(title="Mini-QnA System")

@app.post("/ask", status_code=status.HTTP_200_OK)
async def ask_qna(payload: QnAModel):
    if payload.mode == "baseline":
        raw_results = cosine_search(payload.query, payload.k)
        results = filter_results_by_threshold(raw_results)
    elif payload.mode == 'hybrid-bm25':
        results = hybrid_reranking(payload.query)
    
    answer_with_citations = query_result_with_citations(results)

    return {
        'answer' : answer_with_citations.get('answer'),
        'contexts' : [answer_with_citations.get('citations'), answer_with_citations.get('scores')],
        'mode' : payload.mode
    }

# Run the app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost", 
        port=8000,
        reload=True,
        ws="none"  # Disabled websockets to avoid deprecation warning
    )