## SEMANTIC SEARCH ENGINE FOR INDUSTRIAL PDFS

#### Checklist:
- [x] Got Data from sources.json, added utility to download in `utils`.
- [x] Used `pymupdf` as my PDF loader/reader.
- [x] Added a simple separator based chunker that borrows from Langchain's TextSplitting i.e. using chunk overlapping.
    - Added a tester function to check how well the chunker works in `debug/test_chunking`.
- [x] Added `/ask` API endpoint using FastAPI Backend and Pydantic for validation.
