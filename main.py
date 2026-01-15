"""Red Cross Assistant CLI

Interactive command-line interface for the RAG system.
"""
from ingestion.dataset_loader import load_and_chunk_dataset
from app.rag.database import (
    add_chunk_to_database,
    load_vector_db,
    save_vector_db,
    get_db_size
)
from app.rag.generation import generate_response

DATA_FILE = "data/redcross.txt"
MAX_CHUNK_WORDS = 200
TOP_N = 5


def build_database():
    """Load dataset and build vector database."""
    print("Loading dataset...")
    chunks = load_and_chunk_dataset(DATA_FILE, max_words=MAX_CHUNK_WORDS)

    print(f"Building vector database from {len(chunks)} chunks...")
    for idx, chunk in enumerate(chunks, start=1):
        add_chunk_to_database(chunk)
        if idx % 25 == 0 or idx == len(chunks):
            print(f"  Indexed {idx}/{len(chunks)}")

    save_vector_db()
    print("Database built successfully")


def startup():
    """Initialize the system."""
    print("Red Cross Assistant")
    print("=" * 50)
    
    if load_vector_db():
        print(f"Loaded {get_db_size()} chunks from cache\n")
    else:
        print("No cache found. Building database...\n")
        build_database()
        print()


def chat_loop():
    """Run interactive chat loop."""
    print("Ask me anything about first aid.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            query = input("Your question: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if not query:
            continue

        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = generate_response(query=query, top_n=TOP_N, strict_quotes=False)
        print(f"\n{response}\n")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    startup()
    chat_loop()
