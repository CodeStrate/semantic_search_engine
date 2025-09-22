import pymupdf as pdf
import re
from typing import List

def load_data(document):
    """
    Load PDF using layout-aware extraction and clean OCR artifacts.
    Returns clean, well-structured text ready for chunking.
    """
    full_text = ""
    try:
        doc = pdf.open(document)
        for page in doc:
            # Use blocks for better paragraph structure
            blocks = page.get_text("blocks")
            page_text = ""
            
            # Sort blocks by reading order (top to bottom, left to right)
            blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  # y, then x coordinate
            
            for block in blocks:
                if len(block) >= 5:  # Valid text block
                    block_text = block[4].strip()  # Text content is at index 4
                    if block_text:
                        page_text += block_text + "\n\n"
            
            if page_text.strip():
                full_text += page_text
                
        doc.close()
        
        # Clean the extracted text
        full_text = clean_ocr_text(full_text)
        
    except Exception as e:
        print(f"Error loading PDF from {document} : {e}")

    return full_text.strip()


def clean_ocr_text(text: str) -> str:
    """
    OCR cleaning for the PDF data.
    Handles common OCR artifacts, formatting issues, and technical document quirks.
    """
    # Step 1: Fix hyphenated line breaks
    text = re.sub(r'-\s*\n\s*', '', text)

    # Fix single char cutoffs
    text = re.sub(r'\b([a-zA-Z])\s*\n', r'\1', text)

    # Step 2: Remove table of contents lines (dots + page numbers)
    text = re.sub(r'^.*\.{3,}.*?\d+\s*$', '', text, flags=re.MULTILINE)

    # Step 3: Remove standalone page numbers and section numbers
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\d+\s*$', '', text, flags=re.MULTILINE)

    # Step 4: Fix broken lines
    text = re.sub(r'(?<![.!?:])\n(?!\s*[•\-\d])', ' ', text)

    # Step 5: Clean OCR artifacts
    text = re.sub(r'\xa0', ' ', text)
    text = re.sub(r'\u2003', ' ', text)
    text = re.sub(r'[\u2000-\u200f]', ' ', text)
    text = re.sub(r'[\u2010-\u2015]', '-', text)

    # Step 6: Fix common OCR letter substitutions
    text = re.sub(r'\bngerous\b', 'dangerous', text)
    text = re.sub(r'\bo new\b', 'no new', text)

    # Step 7: Clean up scientific notation
    text = re.sub(r'(\d+)\s*·\s*(\d+)', r'\1 × \2', text)
    text = re.sub(r'(\d+)-(\d+)', r'\1^-\2', text)

    # Step 8: Normalize bullets and numbered lists
    text = re.sub(r'^\s*[•▪▫‣⁃]\s*', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[-]\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*(\d+)\.\s+', r'\1. ', text, flags=re.MULTILINE)

    # Step 9: Fix figure/table references
    text = re.sub(r'Figure\s+(\d+)\.(\d+):', r'Figure \1.\2:', text)
    text = re.sub(r'Table\s+(\d+)\.(\d+):', r'Table \1.\2:', text)

    # Step 10: Whitespace normalization
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'\t+', ' ', text)

    # Step 11: Remove short OCR junk lines
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 5 or any(marker in line.lower() for marker in ['figure', 'table', '•', 'pl ']):
            lines.append(line)
    text = '\n'.join(lines)

    return text.strip()    

def chunk_data(text, chunk_size: int = 400, chunk_overlap: int = 100, separators: List[str] = None):
    """
    Simple and reliable chunker that respects sentence boundaries when possible.
    
    Args:
        text: Document text to split
        chunk_size: Maximum chunk size in characters (default: 400)
        chunk_overlap: Number of characters to overlap (default: 100)
        separators: List of separators to try in order (optional)
    
    Returns:
        List of text chunks
    """
    if not text or len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []
    
    # Default separators prioritize sentence boundaries
    if separators is None:
        separators = [". ", "! ", "? ", "• ", "\n\n", "\n", "; ", ", "]
    
    chunks = []
    start = 0
    text_len = len(text)
    last_end = 0
    
    while start < text_len:
        # Calculate end position
        end = min(start + chunk_size, text_len)
        
        # If we're at the end, just take what's left
        if end == text_len:
            chunk = text[start:end].strip()
            if chunk and len(chunk) > 10:
                chunks.append(chunk)
            break
        
        # Try to find the BEST break point using separators
        best_split = end  # Default to hard cut
        best_separator_priority = len(separators)  # Lower is better
        
        for i, separator in enumerate(separators):
            split_pos = text.rfind(separator, start, end)
            if split_pos > start:
                # Prefer splits closer to our target size, but respect separator priority
                distance_from_target = abs((split_pos + len(separator)) - end)
                
                # Only consider this split if:
                # 1. It's a higher priority separator, OR
                # 2. It's the same priority but closer to target size
                if (i < best_separator_priority or 
                    (i == best_separator_priority and distance_from_target < abs(best_split - end))):
                    best_split = split_pos + len(separator)
                    best_separator_priority = i
        
        # Extract chunk
        chunk = text[start:best_split].strip()
        
        # Only add chunks that are substantial (avoid tiny fragments)
        min_chunk_size = max(50, chunk_size // 8)  # At least 50 chars or 1/8 of target size
        if chunk and len(chunk) >= min_chunk_size:
            chunks.append(chunk)
        
        # Calculate next start position with overlap
        if chunk_overlap > 0 and best_split > start + chunk_overlap:
            start = best_split - chunk_overlap
        else:
            start = best_split
        
        # Safety check to prevent infinite loops
        if start <= last_end:
            start = last_end + 1
        
        last_end = best_split
    
    return chunks


