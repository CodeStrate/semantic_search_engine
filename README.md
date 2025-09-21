## SEMANTIC SEARCH ENGINE FOR INDUSTRIAL PDFS

#### Checklist:
- [] Got Data from sources.json, added utility to download in `utils`.
- [] Used `pymupdf` as my PDF loader/reader.
- [] Added a simple separator based chunker that borrows from Langchain's TextSplitting i.e. using chunk overlapping.
    - Added a tester function to check how well the chunker works in `debug/test_chunking`.
- [] Added chunked data into an SQLite DB. Also added a small query script to validate src and chunks.
- [] Added `/ask` API endpoint using FastAPI Backend and Pydantic for validation.
