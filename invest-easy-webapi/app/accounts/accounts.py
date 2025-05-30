from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from ..db import Base
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_async_session
from ..users import User
from sqlalchemy import select, insert


class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    isActive = Column(Boolean, default=True)


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    accountId = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    isActive = Column(Boolean, default=True)


async def get_user_accounts(session: AsyncSession, user: User):
    result = await session.execute(
        select(Account.id, Account.name)
        .join(
            UserAccount,
            UserAccount.accountId == Account.id and UserAccount.isActive == True,
        )
        .where(UserAccount.userId == user.id and Account.isActive == True)
    )
    return [{"id": str(row[0]), "name": row[1]} for row in result.all()]
