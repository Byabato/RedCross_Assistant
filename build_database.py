"""
Script to build the vector database locally.
Run this before deploying to Railway.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.dataset_loader import load_and_chunk_dataset
from app.rag.database import add_chunk_to_database, save_vector_db, get_db_size, OLLAMA_AVAILABLE

def main():
    print("=" * 70)
    print("Building Vector Database for Red Cross Assistant")
    print("=" * 70)
    
    if not OLLAMA_AVAILABLE:
        print("\n❌ ERROR: Ollama is not available!")
        print("\nTo fix this:")
        print("1. Install Ollama from https://ollama.ai/")
        print("2. Run: ollama pull mistral")
        print("3. Run: ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf")
        print("4. Then run this script again\n")
        sys.exit(1)
    
    data_file = "data/redcross.txt"
    max_words = 200
    
    if not os.path.exists(data_file):
        print(f"\n❌ ERROR: Data file not found: {data_file}\n")
        sys.exit(1)
    
    print(f"\n📖 Loading data from: {data_file}")
    chunks = load_and_chunk_dataset(data_file, max_words=max_words)
    
    if not chunks:
        print("\n❌ ERROR: No chunks loaded from data file\n")
        sys.exit(1)
    
    print(f"✓ Loaded {len(chunks)} chunks\n")
    print("🔄 Embedding chunks (this may take a few minutes)...")
    
    success_count = 0
    for i, chunk in enumerate(chunks, 1):
        if add_chunk_to_database(chunk):
            success_count += 1
        
        if i % 10 == 0 or i == len(chunks):
            print(f"   Progress: {i}/{len(chunks)} chunks processed")
    
    if success_count == 0:
        print("\n❌ ERROR: Failed to embed any chunks\n")
        sys.exit(1)
    
    print(f"\n✓ Successfully embedded {success_count}/{len(chunks)} chunks")
    
    print("\n💾 Saving vector database...")
    save_vector_db()
    
    print(f"✓ Saved {get_db_size()} chunks to data/vector_db.json")
    print("\n" + "=" * 70)
    print("SUCCESS! Vector database is ready for deployment")
    print("=" * 70)
    print("\nNext steps:")
    print("1. git add data/vector_db.json")
    print("2. git commit -m 'Add pre-built vector database'")
    print("3. git push origin main")
    print("4. Deploy to Railway (it will use the pre-built database)")
    print("\n")

if __name__ == "__main__":
    main()
