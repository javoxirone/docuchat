from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from app.db.models import Document
from app.services.ingestion.document import DocumentService, get_document_service

from .schemas import CreateDocumentResponse, RawDocument
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
        document: Document = await service.create_document(raw_document)
        response = CreateDocumentResponse(
            id=document.id,
            original_filename=document.original_filename,
            file_type=document.mime_type,
            file_size_bytes=document.file_size_bytes,
            page_count=document.page_count,
            chunk_count=0,  # This should be updated with the actual chunk count if applicable
            status=document.status,
        )

        return response
    finally:
        await file.close()
