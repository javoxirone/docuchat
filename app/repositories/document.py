from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.document import Document
from app.db.session import async_session_factory


class DocumentRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_documents(self) -> list[Document]:
        stmt = (
            select(Document)
            .options(selectinload(Document.chunks))
            .order_by(Document.created_at.desc())
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def create_document(self, document: Document) -> Document:
        self.db_session.add(document)
        await self.db_session.commit()
        await self.db_session.refresh(document)
        return document

    async def get_document_by_checksum(self, checksum_sha256: str) -> Document:
        stmt = (
            select(Document)
            .filter(Document.checksum_sha256 == checksum_sha256)
            .options(selectinload(Document.chunks))
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_document_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> DocumentRepository:
    return DocumentRepository(db_session)
