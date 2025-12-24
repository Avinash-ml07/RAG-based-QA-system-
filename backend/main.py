from fastapi import FastAPI, UploadFile, File
from backend.ingest import load_policy
from backend.chunker import chunk_policy
from backend.retriever import PolicyRetriever
from backend.generator import GeminiGenerator
from pydantic import BaseModel
import shutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="PolicyGPT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data/policies")
DATA_DIR.mkdir(parents=True, exist_ok=True)

retriever = PolicyRetriever()
generator = GeminiGenerator()


class QueryRequest(BaseModel):
    query: str


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

@app.post("/query")
def query_policy(request: QueryRequest):
    retrieved_chunks = retriever.retrieve(request.query)
    answer = generator.generate_answer(request.query, retrieved_chunks)

    return {
        "answer": answer,
        "sources": retrieved_chunks,
        "retrieved_chunks": len(retrieved_chunks)
    }
