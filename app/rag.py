from pathlib import Path

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from app.config import DATA_DIR, OPENAI_API_KEY, STORAGE_DIR

Settings.llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small", api_key=OPENAI_API_KEY
)

_index: VectorStoreIndex | None = None


def _build_index_from_dir(directory: Path) -> VectorStoreIndex:
    reader = SimpleDirectoryReader(
        input_dir=str(directory),
        recursive=True,
        required_exts=[".pdf", ".txt", ".md"],
    )
    documents = reader.load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=str(STORAGE_DIR))
    return index


def get_index() -> VectorStoreIndex:
    """Load the persisted index or build one from the data directory."""
    global _index
    if _index is not None:
        return _index

    if (STORAGE_DIR / "docstore.json").exists():
        storage_context = StorageContext.from_defaults(
            persist_dir=str(STORAGE_DIR)
        )
        _index = load_index_from_storage(storage_context)
    elif any(DATA_DIR.iterdir()):
        _index = _build_index_from_dir(DATA_DIR)
    else:
        _index = VectorStoreIndex([])

    return _index


def add_documents(file_paths: list[Path]) -> int:
    """Add new documents to the existing index. Returns count of docs added."""
    reader = SimpleDirectoryReader(input_files=[str(p) for p in file_paths])
    documents = reader.load_data()

    index = get_index()
    for doc in documents:
        index.insert(doc)

    index.storage_context.persist(persist_dir=str(STORAGE_DIR))
    return len(documents)


def query(question: str, top_k: int = 3) -> dict:
    """Query the index and return the response with source nodes."""
    index = get_index()
    query_engine = index.as_query_engine(similarity_top_k=top_k)
    response = query_engine.query(question)

    sources = []
    for node in response.source_nodes:
        sources.append(
            {
                "text": node.text[:500],
                "score": round(node.score, 4) if node.score else None,
                "metadata": node.metadata,
            }
        )

    return {"answer": str(response), "sources": sources}
