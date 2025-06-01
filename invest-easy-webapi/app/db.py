# Database setup
from collections.abc import AsyncGenerator
import uuid
from fastapi import Depends
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)

DATABASE_URL = f"sqlite+aiosqlite:///./db/easy.db"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


# User model
class User(SQLAlchemyBaseUserTableUUID, Base):
    username = mapped_column(String(30), unique=True, nullable=False)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


# Create tables function
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# Database setup
async def get_user_db():
    async with async_session_maker() as session:
        yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
