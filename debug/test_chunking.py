from chunk_db.chunk_data import chunk_data
# Test function

def test_chunker():
    """Test the data chunker with sample text."""
    sample_text = """
    This is a sample document with multiple paragraphs. This paragraph talks about the first topic.
    
    This is the second paragraph. It discusses another important topic. The sentences here are meant to test the splitting logic.
    
    This is the third paragraph. It has some very long sentences that might need to be split further if the chunk size is small.
    """

    # Test different overlaps
    overlaps=[40, 80, 120]

    for overlap in overlaps:
        chunks = chunk_data(sample_text, chunk_size=150, chunk_overlap=overlap)
        print(f"\n--- overlap={overlap}, total chunks={len(chunks)} ---")
        for i, c in enumerate(chunks[:3]):  # show first 3 chunks
            print(f"[{i}] {c[:120]}...")  # truncate for display

    # Test normal chunking
    
    # chunks = chunk_data(sample_text, chunk_size=150, chunk_overlap=30, separators=[". "])
    
    # print(f"Original text length: {len(sample_text)}")
    # print(f"Number of chunks: {len(chunks)}")
    # for i, chunk in enumerate(chunks):
    #     print(f"Chunk {i+1} ({len(chunk)} chars): {chunk[:50]}...")

if __name__ == '__main__':
    test_chunker()