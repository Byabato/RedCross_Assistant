import ollama
import json
import os
import sys

# Model configuration
EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'mistral'

# In-memory vector database
VECTOR_DB = []
DB_FILE = "data/vector_db.json"

# Check Ollama availability
OLLAMA_AVAILABLE = False
try:
    ollama.list()
    OLLAMA_AVAILABLE = True
    print("✓ Ollama is available")
except Exception:
    print("⚠ Ollama not available - using pre-built vector database only")
    print("  This is normal on cloud deployments (Railway, Heroku, etc.)")


def add_chunk_to_database(chunk):
    """Embed a text chunk and store it in the vector database."""
    if not OLLAMA_AVAILABLE:
        print("Cannot add chunks without Ollama. Please build database locally first.")
        return False
    
    try:
        result = ollama.embed(model=EMBEDDING_MODEL, input=chunk)
        embedding = result['embeddings'][0]
        VECTOR_DB.append((chunk, embedding))
        return True
    except Exception as e:
        print(f"Error embedding chunk: {e}")
        return False


def save_vector_db():
    """Save the vector database to disk."""
    try:
        os.makedirs("data", exist_ok=True)
        with open(DB_FILE, 'w') as f:
            json.dump(VECTOR_DB, f)
        print(f"Saved {len(VECTOR_DB)} chunks to cache")
    except Exception as e:
        print(f"Error saving database: {e}")


def load_vector_db():
    """Load the vector database from disk if it exists."""
    global VECTOR_DB
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f:
                VECTOR_DB = json.load(f)
            print(f"✓ Loaded {len(VECTOR_DB)} chunks from cache")
            if len(VECTOR_DB) == 0:
                print("⚠ Warning: Vector database is empty!")
                return False
            return True
        else:
            print(f"⚠ Vector database file not found: {DB_FILE}")
    except Exception as e:
        print(f"✗ Error loading database: {e}")
    return False


def get_db_size():
    """Return the number of chunks in the database."""
    return len(VECTOR_DB)
