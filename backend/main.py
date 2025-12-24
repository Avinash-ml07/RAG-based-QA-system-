from fastapi import FastAPI, UploadFile, File
from backend.ingest import load_policy
from backend.chunker import chunk_policy
import shutil
from pathlib import Path

app = FastAPI(title="PolicyGPT")

DATA_DIR = Path("data/policies")
DATA_DIR.mkdir(parents=True, exist_ok=True)


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

    return {
        "message": "Policy uploaded successfully",
        "chunks_created": len(chunks),
    }
