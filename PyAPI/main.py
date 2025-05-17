from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}