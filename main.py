from fastapi import FastAPI

app = FastAPI(title="PDF Processing API", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "PDF Processing API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}