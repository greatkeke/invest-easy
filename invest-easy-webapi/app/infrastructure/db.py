# Database setup
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any, Hashable
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, String, JSON
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from ..domain.users import User, AccessToken
from ..domain.base_domain import Base
from sqlalchemy import update


class StockBasicInfoCache(Base):
    """Table for caching stock basic info from Futu API"""

    __tablename__ = "stock_basic_info_cache"

    market = Column(String, primary_key=True)
    stock_type = Column(String, primary_key=True)
    data = Column(JSON)

    def is_expired(self) -> bool:
        """Check if cache is older than 1 day"""
        if self.created_at is None:
            return True
        delta = datetime.now() - self.created_at
        return delta.days >= 1


DATABASE_URL = f"sqlite+aiosqlite:///./db/easy.db"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


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


async def get_stock_basicinfo_cache(
    session: AsyncSession, market: str, stock_type: str
) -> StockBasicInfoCache | None:
    """Get cached stock basic info if exists and not expired"""
    cache = await session.get(
        StockBasicInfoCache, {"market": market, "stock_type": stock_type}
    )
    if cache and not cache.is_expired():
        return cache
    return None


async def update_stock_basicinfo_cache(
    session: AsyncSession, market: str, stock_type: str, data: list[dict[Hashable, Any]]
) -> StockBasicInfoCache:
    """Update or create stock basic info cache"""

    # Get the updated or new cache entry
    cache = await session.get(
        StockBasicInfoCache, {"market": market, "stock_type": stock_type}
    )

    if cache is None:
        # If no existing entry, create new one
        cache = StockBasicInfoCache(
            market=market,
            stock_type=stock_type,
            data=data,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
        )
        session.add(cache)
        await session.commit()
        await session.refresh(cache)
    else:
        # try to update existing cache
        stmt = (
            update(StockBasicInfoCache)
            .where(StockBasicInfoCache.market == market)
            .where(StockBasicInfoCache.stock_type == stock_type)
            .values(data=data, created_at=datetime.now(), updated_at=datetime.now())
        )
        await session.execute(stmt)
        await session.commit()

    return cache
