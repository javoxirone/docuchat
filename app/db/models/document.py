import uuid
from datetime import datetime

from sqlalchemy import UUID, BigInteger, DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    __table_args__ = (
        UniqueConstraint("checksum_sha256", name="uq_documents_checksum_sha256"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)

    # file type like: pdf, docx, txt, etc. in other words just short extension of the file
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)

    # the official internet media type standard that consists of a type and subtype,
    # like: application/pdf, text/plain, image/jpeg, etc.
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"Document(\
        id={self.id}, \
        original_filename={self.original_filename}, \
        file_type={self.file_type}, \
        mime_type={self.mime_type}, \
        file_size_bytes={self.file_size_bytes}, \
        checksum_sha256={self.checksum_sha256}, \
        page_count={self.page_count}, \
        status={self.status}, \
        error_code={self.error_code}, \
        created_at={self.created_at}, \
        updated_at={self.updated_at})"
