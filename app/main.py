import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import DATA_DIR
from app.rag import add_documents, query

app = FastAPI(title="RAG API", description="RAG application powered by LlamaIndex")

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


@app.post("/upload")
async def upload_files(files: list[UploadFile]):
    """Upload PDF, TXT, or MD files to the knowledge base."""
    allowed_exts = {".pdf", ".txt", ".md"}
    saved_paths: list[Path] = []

    for file in files:
        ext = Path(file.filename).suffix.lower()
        if ext not in allowed_exts:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {ext}. Allowed: {allowed_exts}",
            )

        dest = DATA_DIR / file.filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_paths.append(dest)

    count = add_documents(saved_paths)
    return {"message": f"Indexed {count} document chunks from {len(files)} file(s)."}


@app.post("/query", response_model=QueryResponse)
async def query_documents(req: QueryRequest):
    """Ask a question against the indexed documents."""
    result = query(req.question, top_k=req.top_k)
    return result


@app.get("/health")
async def health():
    return {"status": "ok"}
