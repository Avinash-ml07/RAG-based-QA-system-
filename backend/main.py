from fastapi import FastAPI, UploadFile, File
from backend.ingest import load_policy
from backend.chunker import chunk_policy
from backend.retriever import PolicyRetriever
import shutil
from pathlib import Path

app = FastAPI(title="PolicyGPT")

DATA_DIR = Path("data/policies")
DATA_DIR.mkdir(parents=True, exist_ok=True)

retriever = PolicyRetriever()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload-policy")
async def upload_policy(file: UploadFile = File(...)):
    file_path = DATA_DIR / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = load_policy(str(file_path))
    chunks = chunk_policy(text)

    retriever.build_index(chunks)

    return {
        "message": "Policy uploaded and indexed",
        "chunks_indexed": len(chunks),
    }


@app.post("/retrieve")
def retrieve_policy(query: str):
    results = retriever.retrieve(query)
    return {"retrieved_chunks": results}
