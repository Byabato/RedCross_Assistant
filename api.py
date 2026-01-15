"""Red Cross Assistant API

A FastAPI server that provides RAG-based first aid guidance.
"""
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ingestion.dataset_loader import load_and_chunk_dataset
from app.rag.database import (
    add_chunk_to_database,
    load_vector_db,
    save_vector_db,
    get_db_size,
)
from app.rag.generation import generate_response

# Configuration
DATA_FILE = "data/redcross.txt"
MAX_CHUNK_WORDS = 200
DEFAULT_TOP_N = 5
DEFAULT_STRICT = False
DEFAULT_DEBUG = False

app = FastAPI(title="Red Cross Assistant", version="1.0.0")


class ChatRequest(BaseModel):
    query: str
    top_n: int | None = None
    strict_quotes: bool | None = None
    debug: bool | None = None


class ChatResponse(BaseModel):
    response: str


# Mount static files
WEB_DIR = Path(__file__).parent / "web"
WEB_DIR.mkdir(exist_ok=True)
app.mount("/web", StaticFiles(directory=str(WEB_DIR)), name="web")


@app.on_event("startup")
async def startup():
    """Load or build the vector database on startup."""
    print("=" * 60)
    print("Red Cross Assistant - Starting up...")
    print("=" * 60)
    
    # Try to load existing database
    if load_vector_db():
        print(f"✓ Vector database ready with {get_db_size()} chunks")
        print("=" * 60)
        return
    
    print("⚠ No pre-built vector database found")
    
    # Check if we can build it
    from app.rag.database import OLLAMA_AVAILABLE
    if not OLLAMA_AVAILABLE:
        print("✗ Cannot build database without Ollama")
        print("")
        print("SOLUTION:")
        print("1. Run locally with Ollama installed: python api.py")
        print("2. This will generate data/vector_db.json")
        print("3. Commit and push vector_db.json to your repo")
        print("4. Redeploy to Railway")
        print("=" * 60)
        raise RuntimeError(
            "Vector database not found and Ollama not available. "
            "Please build the database locally first (see startup logs)."
        )
    
    # Build database if Ollama is available
    if not os.path.exists(DATA_FILE):
        raise RuntimeError(f"Data file not found: {DATA_FILE}")
    
    print(f"Building vector database from {DATA_FILE}...")
    chunks = load_and_chunk_dataset(DATA_FILE, max_words=MAX_CHUNK_WORDS)
    
    if not chunks:
        raise RuntimeError("No chunks loaded from data file")
    
    success_count = 0
    for i, chunk in enumerate(chunks, 1):
        if add_chunk_to_database(chunk):
            success_count += 1
        if i % 10 == 0:
            print(f"  Processed {i}/{len(chunks)} chunks...")
    
    if success_count == 0:
        raise RuntimeError("Failed to embed any chunks")
    
    save_vector_db()
    print(f"✓ Vector database built with {get_db_size()} chunks")
    print("=" * 60)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "chunks": get_db_size(),
    }


@app.get("/", response_class=HTMLResponse)
def index():
    """Serve the main UI."""
    index_file = WEB_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Red Cross Assistant</h1><p>UI not found.</p>")
    return HTMLResponse(index_file.read_text(encoding="utf-8"))


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Process a user query and return a response."""
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    response = generate_response(
        query=query,
        top_n=request.top_n or DEFAULT_TOP_N,
        strict_quotes=DEFAULT_STRICT if request.strict_quotes is None else request.strict_quotes,
        debug=DEFAULT_DEBUG if request.debug is None else request.debug,
    )
    return ChatResponse(response=response)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
