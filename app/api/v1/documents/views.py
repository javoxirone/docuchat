from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from app.db.models import Document
from app.services.ingestion.document import DocumentService, get_document_service

from .schemas import CreateDocumentResponse, GetDocumentsItemResponse, RawDocument
from .validators import validate_file

router = APIRouter()


@router.post("/v1/documents/", tags=["documents"], response_model=CreateDocumentResponse)
async def create_document(
    file: Annotated[UploadFile, Depends(validate_file)],
    service: Annotated[DocumentService, Depends(get_document_service)],
):

    try:
        raw_document = RawDocument(
            filename=file.filename, content_type=file.content_type, content=await file.read()
        )
        document: Document = await service.get_or_create_document(raw_document)

        return document
    finally:
        await file.close()


@router.get("/v1/documents/", tags=["documents"], response_model=list[GetDocumentsItemResponse])
async def get_documents(
    service: Annotated[DocumentService, Depends(get_document_service)],
):
    documents: list[Document] = await service.get_documents()
    return documents
