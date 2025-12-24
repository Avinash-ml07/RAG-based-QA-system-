from fastapi import FastAPI

app = FastAPI(title="PolicyGPT")

@app.get("/health")
def health():
    return {"status": "healthy"}
