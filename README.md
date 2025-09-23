# Semantic Search Engine

## NOTE: Sample chunked SQLite DB and Chroma DB are added so API can be directly tested.

A semantic search engine for machinery safety documents that combines vector similarity search with BM25 lexical search for improved retrieval accuracy.

## Project Structure

```
semantic_search_engine/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── qna_model.py         # Pydantic models for API
├── chunk_db/
│   ├── __init__.py
│   ├── chunk_data.py        # PDF processing and text chunking
│   ├── ingest_chunks.py     # Chunk storage and vector embedding
│   └── ingest_into_db.py    # Database ingestion pipeline
├── sourced_data/
│   └── *.pdf               # Source PDF documents
├── hybrid_reranker/
│   ├── __init__.py
│   └── bm25_reranker.py    # BM25 + vector hybrid search
├── utils/
│   ├── __init__.py
│   ├── common_utils.py          # Commonly used utilities in this app
│   ├── download_source_data.py  # Data download script
│   ├── normalize_scores.py      # Score normalization utilities
│   └── retrieval_utils.py       # Answer formatting and citations
├── vector_db/
│   ├── __init__.py
│   └── baseline_search.py   # Vector similarity search
├── sources.json             # Data source configuration
└── README.md
```

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/CodeStrate/semantic_search_engine.git
cd semantic_search_engine
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Setup and Usage

### 1. Download Data
```bash
python utils/download_source_data.py
```
This downloads PDF documents specified in `sources.json` to the `data/` directory.

### 2. Chunk and Ingest Data
```bash
python -m chunk_db.ingest_into_db
```
This processes PDFs, extracts text with OCR cleaning, and creates text chunks with metadata.

### 3. Embed and Store in ChromaDB
```bash
python -m chunk_db.ingest_chunks
```
This generates embeddings using `all-MiniLM-L6-v2` (it also downloads it if not available for ChromaDB) and stores them in ChromaDB for vector search.

### 4. Start the API Server
```bash
python api/main.py
```
The FastAPI server will start on `http://localhost:8000`

## API Endpoints

### POST `/ask`

Submit a query and get an answer with citations.

**Request Body**:
```json
{
  "query": "What is OSHA?",
  "k": 5,
  "mode": "baseline"
}
```

**Parameters**:
- `query` (string, required): User's question
- `k` (integer, optional): Number of chunks to retrieve (default: 5)
- `mode` (string, optional): Search mode - `"baseline"` or `"hybrid-bm25"` (default: `"baseline"`)

**Response**:
```json
{
  "answer": "OSHA is the Occupational Safety and Health Administration...",
  "contexts": [
    [
      {
        "chunk_id": "123",
        "src_id": "src01",
        "title": "OSHA Guidelines",
        "url": "https://example.com/osha.pdf",
        "score": 0.95
      }
    ],
    [0.95, 0.87, 0.82]
  ],
  "mode": "baseline"
}
```

## Curl Requests

### Basic Query
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is OSHA?",
    "k": 5,
    "mode": "baseline"
  }'
```

### Hybrid Search Query (tricky)
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machinery safety regulations and compliance requirements",
    "k": 10,
    "mode": "hybrid-bm25"
  }'
```

### Off-topic Query (to test abstinence)
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "hello how are you today?",
    "k": 5,
    "mode": "baseline"
  }'
```

## Testing

Test individual components or `debug/` snippets:

```bash
# Test baseline search
python -m vector_db.baseline_search

# Test hybrid reranking
python -m hybrid_reranker.bm25_reranker
```
Each component is independently testable and can be run as a module using Python's `-m` flag.

# Learnings
While it seems easy (just chunk, embed and retrieve) it's not, a lot of time was spent on tuning the chunking functionality, especially when the **PDFs** are **OCR based** so the PDF text extraction is never perfect and given the limitations I had to spend a lot of test_chunking iterations just to find a good chunk spot. It is the same reason I chose to pursue `Langchain`'s Chunking methodology with separators and overlaps to make sure my chunks are context aware on their own as we can't use a generative model (`generation`) here. While it works well, there are still some **tricky** queries that can stump my retriever. **Chunking** needs more testing and time. I saw how some harder queries didn't even return an answer due to my `abstain` filter. Which I had to increase.

If I could use generation then `retrieval_utils` and **Regex based OCR cleaning is not required** (at all). This project taught me the power of generative LLMs and how they can seemingly do anything that's told to. Given use-case doesn't require a **Paid** API though, I am sure a `1B` Ollama or HuggingFace model would suffice. I also finally learned how to add citations in retrieval through `metadata` (from Chroma Docs). While I saw `rank-bm25` was the most used bm25 implementation, I saw `bm25s` in a HuggingFace Blog and was fascinated by its lightweighted-ness. To further make the project lightweight I chose not to use many NLP based libraries which might have affected my result quality. Using `Chroma` and `PyMuPDF` were my personal choices given my previous experience using them. We could have definitely reduced some weight with `FAISS` but then `SentenceTransformers` is required which has a dependency on `torch` and other heavy dependencies. It didn't seem worth it.
