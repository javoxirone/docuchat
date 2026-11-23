from fastapi import FastAPI

from app.api.v1.documents import router as documents_router

app = FastAPI(
    title="DocuChat API",
    description="AI-powered document assistant using RAG",
    version="0.1.0",
)

app.include_router(documents_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
