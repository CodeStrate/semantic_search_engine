import pymupdf as pdf, os
from tqdm import tqdm
from typing import List

def load_from_src(src_dir: str = "sourced_data"):
    all_docs = []
    if os.path.exists(src_dir):
        for file in tqdm(os.listdir(src_dir), desc=f"Loading documents from {src_dir}"):
            try:
                file_path = os.path.join(src_dir, file)
                doc = pdf.open(file_path)
                all_docs.extend(doc)
                print(f"Loaded document successfully - {file}")
            except Exception as e:
                print(f"Error loading document {file} - {e}")

    return all_docs

def load_data(doc):
    full_text = "\n\n".join([page.get_text() for page in doc])
    return full_text
    

def chunk_data(text, chunk_size: int = 400, chunk_overlap: int = 50, separators: List[str] = None):
    """
    Chunk text splitter function to split text using different separators.
    Args:
    text = Document to split
    chunk_size: int: Maximum size of each chunk in characters, defaults to 400
    chunk_overlap: int: Number of characters to overlap between chunks, defaults to 50
    separators: List[str] = List of sentence separators. eg. ".", ",", "\n"
    
    Returns:
        List of text chunks

    """
    # Base case: text is already small enough
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []
    
    chunks = []
    start = 0
    n = len(text)

    if separators is None:
        while start < n:
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            # change start wrt overlap
            start = end - chunk_overlap
        
        return chunks

    while start < n:
        end = min(start + chunk_size, n)
        # try to split using a separator

        split_at_sep = None
        for sep in separators:
            index = text.rfind(sep, start, end) # highest index where its found
            if index != -1 and index > start:
                split_at_sep = index + len(sep)
                break
        
        # no separator was found
        if split_at_sep is None:
            split_at_sep = end

        chunk = text[start:split_at_sep].strip()
        if chunk:
            chunks.append(chunk)

        start = split_at_sep - chunk_overlap if split_at_sep - chunk_overlap > start else split_at_sep

    return chunks


