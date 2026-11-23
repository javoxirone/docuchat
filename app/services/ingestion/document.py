from hashlib import sha256
from typing import Annotated, Any

from fastapi import Depends

from app.api.v1.documents.schemas import RawDocument
from app.api.v1.documents.utils import get_file_extension
from app.db.models.document import Document
from app.repositories.document import DocumentRepository, get_document_repository


class DocumentService:
    def __init__(self, repository):
        self.repository = repository

    async def create_document(self, raw_document: RawDocument) -> Any:
        original_filename = raw_document.filename
        file_type = get_file_extension(raw_document.filename)
        mime_type = raw_document.content_type
        checksum_sha256 = sha256(raw_document.content).hexdigest()
        document = Document(
            original_filename=original_filename,
            file_type=file_type,
            mime_type=mime_type,
            file_size_bytes=len(raw_document.content),
            checksum_sha256=checksum_sha256,
            page_count=None,  # This should be updated with the actual page count if applicable
            status="pending",  # This should be updated with the actual status if applicable
            error_code=None,  # This should be updated with the actual error code if applicable
        )
        return await self.repository.create_document(document)


async def get_document_service(
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
) -> DocumentService:
    return DocumentService(repository)
