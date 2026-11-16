# LlamaIndex RAG App

A minimal retrieval-augmented generation (RAG) API built with LlamaIndex and FastAPI: upload documents, index them, and ask questions over them.

## Features

- Builds a `VectorStoreIndex` from files in `data/` and persists it to `storage/`
- `POST /upload` to add files to the index
- `POST /query` to ask a question (configurable `top_k`) and get an answer with sources
- `GET /health` health check
- Simple HTML UI served at `/`

## Tech stack

Python, FastAPI, LlamaIndex, OpenAI (`gpt-4o-mini` LLM, `text-embedding-3-small` embeddings), python-dotenv.

## Project structure

```
app/
  main.py      # FastAPI routes
  rag.py       # Index build/load, add documents, query
  config.py    # Env loading and paths
  static/      # index.html UI
data/          # Source documents (sample.txt included)
storage/       # Persisted index (generated, git-ignored)
run.sh         # Creates venv, installs deps, starts server
```

## Setup

```bash
cp .env.example .env   # add your OpenAI key
./run.sh
```

Or manually:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000 (API docs at `/docs`).

## Configuration

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Required. Used for the LLM and embeddings. |

## Status

Learning/demo project.
