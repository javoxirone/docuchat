import uuid
from datetime import datetime

# the value is False at runtime, but True while type checking
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import UUID, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models.document import Document

from app.db.base import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            "document_id", "chunk_index", name="uq_document_chunks_document_id_and_chunk_index"
        ),
        Index("ix_document_chunks_document_id", "document_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document: Mapped["Document"] = relationship(back_populates="chunks")

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)

    # might be true because plain text does not have pages
    page_number: Mapped[int] = mapped_column(Integer, nullable=True)

    char_start: Mapped[int] = mapped_column(Integer, nullable=True)
    char_end: Mapped[int] = mapped_column(Integer, nullable=True)

    content: Mapped[str] = mapped_column(String, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(VECTOR(768), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"DocumentChunk(\
        id={self.id}, \
        document_id={self.document_id}, \
        chunk_index={self.chunk_index}, \
        page_number={self.page_number}, \
        char_start={self.char_start}, \
        char_end={self.char_end}, \
        content={self.content}, \
        embedding={self.embedding}, \
        created_at={self.created_at})"
