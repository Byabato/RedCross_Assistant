import re


def load_and_chunk_dataset(file_path, max_words=200):
    """
    Load a text file and split it into smaller chunks.
    
    Args:
        file_path: Path to the text file
        max_words: Maximum words per chunk
        
    Returns:
        List of text chunks
    """
    chunks = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Split by paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        
        # Break paragraphs into chunks
        for para in paragraphs:
            words = para.split()
            for i in range(0, len(words), max_words):
                chunk = " ".join(words[i:i+max_words])
                chunks.append(chunk)
        
        print(f"Loaded {len(chunks)} chunks from {file_path}")
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
    
    return chunks
