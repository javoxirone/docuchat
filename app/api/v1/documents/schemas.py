import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateDocumentResponse(BaseModel):
    id: uuid.UUID = Field(description="The unique identifier of the created document")
    original_filename: str = Field(description="The original name of the uploaded file")
    file_type: str = Field(description="The type of the uploaded file (e.g., pdf or txt)")
    file_size_bytes: int = Field(description="The size of the uploaded file in bytes")
    page_count: int | None = Field(
        description="The number of pages in the uploaded file, if applicable"
    )
    chunk_count: int = Field(description="The number of chunks the document was split into")
    status: str = Field(description="The status of the document processing")

    model_config = ConfigDict(
        from_attributes=True,
    )


class GetDocumentsItemResponse(BaseModel):
    id: uuid.UUID = Field(description="The unique identifier of the document")
    original_filename: str = Field(description="The original name of the uploaded file")
    file_type: str = Field(description="The type of the uploaded file (e.g., pdf or txt)")
    chunk_count: int = Field(description="The number of chunks the document was split into")
    page_count: int | None = Field(
        description="The number of pages in the uploaded file, if applicable"
    )
    status: str = Field(description="The status of the document processing")
    created_at: datetime = Field(description="The timestamp when the document was created")

    model_config = ConfigDict(
        from_attributes=True,
    )


class RawDocument(BaseModel):
    filename: str | None = Field(description="The name of the uploaded file")
    content_type: str | None = Field(description="The MIME type of the uploaded file")
    content: bytes = Field(description="The content of the uploaded file in bytes")
