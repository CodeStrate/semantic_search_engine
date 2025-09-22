## SEMANTIC SEARCH ENGINE FOR INDUSTRIAL PDFS

#### Checklist:
- [x] Got Data from sources.json, added utility to download in `utils`.
- [x] Used `pymupdf` as my PDF loader/reader.
- [x] Added a simple separator based chunker that borrows from Langchain's TextSplitting i.e. using chunk overlapping.
    - Added a tester function to check how well the chunker works in `debug/test_chunking`.
- [x] Added chunked data into an SQLite DB. Also added a small query script to validate src and chunks.
- [x] Added `ChromaDB` as my vector store. Why? it embeds queries and chunks on its own using `all-MiniLM-L6-v2` by default. So, we dont require `SentenceTransformers` and its dependencies. saving on project library weightage.
- [x] Added a `BM25` reranker using `bm25s` library.
- [x] Added a baseline Search from the vector DB. Simple cosine top-k.
- [x] Added `/ask` API endpoint using FastAPI Backend and Pydantic for validation.
- [ ] Remaining Tasks :
    - adding a function to `abstain` responses.
    - a function to return 2-3 sentences from either search/reranker.
    - Completing the `/ask` endpoint.
