from typing import List
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, text
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..db import Base
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_async_session
from ..users import User
from sqlalchemy import select, insert
from sqlalchemy.orm import Mapped


class Account(Base):
    __tablename__ = "accounts"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String, nullable=False)
    ccy = mapped_column(String(3), nullable=False, server_default=text("HKD"))
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = mapped_column(Boolean, default=True)


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    account_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False
    )
    created_at = mapped_column(DateTime, server_default=func.now())
    is_active = mapped_column(Boolean, default=True)
    balances: Mapped[List["Balance"]] = relationship(
        "Balance", back_populates="user_account"
    )


async def get_user_accounts(session: AsyncSession, user: User):
    result = await session.execute(
        select(Account.id, Account.name)
        .join(
            UserAccount,
            UserAccount.account_id == Account.id and UserAccount.is_active == True,
        )
        .where(UserAccount.user_id == user.id and Account.is_active == True)
    )
    return [{"id": str(row[0]), "name": row[1]} for row in result.all()]
