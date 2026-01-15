import ollama
from app.rag import database


def cosine_similarity(vec_a, vec_b):
    """Calculate cosine similarity between two vectors."""
    try:
        dot_product = sum(x * y for x, y in zip(vec_a, vec_b))
        norm_a = sum(x ** 2 for x in vec_a) ** 0.5
        norm_b = sum(x ** 2 for x in vec_b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0


def retrieve(query, top_n=5):
    """
    Find the most relevant chunks for a given query.
    
    Args:
        query: User's question
        top_n: Number of chunks to return
        
    Returns:
        List of (chunk_text, similarity_score) tuples
    """
    try:
        if not database.VECTOR_DB:
            return []
        
        # Embed the query
        query_embedding = ollama.embed(
            model=database.EMBEDDING_MODEL,
            input=query
        )['embeddings'][0]
        
        # Calculate similarity for each chunk
        similarities = []
        for chunk, embedding in database.VECTOR_DB:
            score = cosine_similarity(query_embedding, embedding)
            similarities.append((chunk, score))
        
        # Sort by similarity and return top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]
        
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []
