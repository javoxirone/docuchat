from fastapi import FastAPI

app = FastAPI(
    title="DocuChat API",
    description="AI-powered document assistant using RAG",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
