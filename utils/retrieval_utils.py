import re
# for word completion fixing
from spellchecker import SpellChecker

def format_answer(text:str, n_sentences:int=2, minimum_word_count:int=4) -> str:
    """Format out a 2-3 sentence answer from the provided document text"""
    formatted_answer = []
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    for sentence in sentences:
        if len(sentence.split(" ")) >= minimum_word_count:
            formatted_answer.append(sentence.strip())
        
        if len(formatted_answer) >= n_sentences:
            break
    return " ".join(formatted_answer)


# why? since words are cut off in the beginning and we handled end cutoff by formatting sentences.
def fix_first_word_cutoff(text: str) -> str:
    """Fix OCR cutoff issues in the first word only."""
    words = text.split()
    if not words:
        return text
    
    first_word = words[0]
    
    # If first word starts with lowercase and is likely a cutoff, try to fix it
    # i.e. its not a proper noun or acronym
    if first_word[0].islower() and len(first_word) > 2:
        spell = SpellChecker()
        clean_word = "".join(ch for ch in first_word if ch.isalpha())
        
        if clean_word.lower() not in spell:
            suggestion = spell.correction(clean_word)
            if suggestion:
                # Capitalize the suggestion since it's likely a proper noun
                words[0] = suggestion.capitalize()

    # capitalize regardless
    words[0] = words[0].capitalize()
    return " ".join(words)


def query_result_with_citations(result) -> dict:
    """
    Format an answer + citation from top 3 results.
    
    Args:
    result: Dictionary with structure like from hybrid_reranking:
            [(doc, meta, score), (doc, meta, score), ...]
            OR from cosine_search with 'documents' and 'metadatas' keys
    
    Returns:
        dict: {
            'answer': str,
            'citations': list,
            'scores': list
        }
    """
    # Handle different input formats
    if isinstance(result, list):
        # Format from hybrid_reranking
        if not result:
            return {'answer': None, 'citations': [], 'scores': []}
        
        top_chunks = result[:3]
        docs = [chunk[0] for chunk in top_chunks]
        metas = [chunk[1] for chunk in top_chunks]
        scores = [chunk[2] for chunk in top_chunks]
    else:
        # Format from baseline search
        docs = result.get('documents', [[]])[0][:3]
        metas = result.get('metadatas', [[]])[0][:3]
        distances = result.get('distances', [[]])[0][:3]
        scores = [1 - dist for dist in distances]
    
    if not docs:
        return {'answer': None, 'citations': [], 'scores': []}
    
    # Process multiple chunks
    formatted_answers = []
    citations = []
    
    for doc, meta, score in zip(docs, metas, scores):
        # Format answer and fix text issues
        answer = format_answer(doc, n_sentences=2)
        answer = fix_first_word_cutoff(answer)
        formatted_answers.append(answer)
        
        # Create citation for this chunk
        citation = {
            'chunk_id': meta.get('chunk_id', 'Unknown'),
            'src_id': meta.get('source_id', 'unknown'),
            'title': meta.get('title', 'Unknown Document'), 
            'url': meta.get('url', ''),
            'score': score
        }
        citations.append(citation)
    
    # Combine all answers
    final_answer = ' '.join(formatted_answers)

    # shorten the answer further for readability but retain citations.
    short_answer = format_answer(final_answer)

    return {
        'answer': short_answer,
        'citations': citations,
        'scores': scores
    }
