from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.db.session import async_session_factory


class DocumentRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_document(self, document: Document) -> Document:
        self.db_session.add(document)
        await self.db_session.commit()
        await self.db_session.refresh(document)
        return document


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_document_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> DocumentRepository:
    return DocumentRepository(db_session)
