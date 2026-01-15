# Red Cross Assistant

An AI-powered first aid assistant that provides guidance based on official Red Cross training materials using RAG (Retrieval-Augmented Generation).

## Features

- **Conversational AI**: Natural, human-like responses powered by LLM
- **Strict Quote Mode**: Direct quotes from source material
- **Web Interface**: Professional, user-friendly UI
- **CLI Tool**: Command-line interface for quick access
- **Vector Search**: Fast semantic search across Red Cross materials
- **Caching**: Instant startup after first run

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running
- Ollama models: `mistral` and `hf.co/CompendiumLabs/bge-base-en-v1.5-gguf`

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd MyRAG

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull required Ollama models
ollama pull mistral
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
```

### Usage

**Web Interface** (Recommended):
```bash
python api.py
```
Then open http://localhost:8000

**Command Line**:
```bash
python main.py
```

## Project Structure

```
MyRAG/
├── app/
│   └── rag/
│       ├── database.py      # Vector database management
│       ├── retrieval.py     # Semantic search
│       └── generation.py    # Response generation
├── ingestion/
│   └── dataset_loader.py    # Text chunking
├── web/
│   ├── index.html          # UI
│   └── favicon.svg         # Red Cross icon
├── data/
│   └── redcross.txt        # Source material
├── api.py                  # FastAPI server
├── main.py                 # CLI interface
└── requirements.txt        # Dependencies
```

## Configuration

Edit these constants in `api.py` or `main.py`:

- `DATA_FILE`: Path to your source material
- `MAX_CHUNK_WORDS`: Chunk size for text splitting
- `DEFAULT_TOP_N`: Number of chunks to retrieve
- `DEFAULT_STRICT`: Use strict quotes vs conversational

## How It Works

1. **Ingestion**: Splits Red Cross materials into chunks
2. **Embedding**: Converts chunks to vectors using Ollama
3. **Storage**: Caches vectors for fast retrieval
4. **Retrieval**: Finds relevant chunks via cosine similarity
5. **Generation**: LLM creates natural responses from chunks

## Response Modes

**Conversational** (default): LLM generates human-friendly explanations while staying grounded in source material.

**Strict Quotes**: Returns direct quotes formatted as numbered points.

## Deployment

### Local

```bash
python api.py
```

### Production

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## License

This project is for educational purposes. Red Cross materials are used under fair use for training.

## Contributing

Contributions welcome! Please open an issue or PR.

## Acknowledgments

- Built with FastAPI, Ollama, and modern RAG techniques
- Red Cross training materials for source content
