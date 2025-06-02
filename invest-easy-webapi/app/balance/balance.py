from datetime import datetime
from typing import List
import uuid
from fastapi import Depends
from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import (
    UUID,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    select,
    text,
    update,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base, AsyncSession, get_async_session
from ..accounts.accounts import UserAccount


class Balance(Base):
    __tablename__ = "balances"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_account_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_accounts.id"), nullable=False
    )
    balance = mapped_column(Float, nullable=False, default=0.00)
    ccy = mapped_column(String(3), nullable=False, default="HKD")
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    user_account = relationship("UserAccount", back_populates="balances")
    balance_histories: Mapped[List["BalanceHistory"]] = relationship(
        "BalanceHistory", back_populates="balance"
    )


class BalanceHistory(Base):
    __tablename__ = "balance_histories"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("balances.id"), nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    ccy = mapped_column(String(3), nullable=False)
    transfer_in = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    balance = relationship("Balance", back_populates="balance_histories")


async def transfer_in_amount(
    transfer_user_id: uuid.UUID,
    account_id: uuid.UUID,
    amount: float,
    ccy: str,
    session: AsyncSession,
    transfer_in=True,
):
    try:
        user_account = await session.scalars(
            select(UserAccount).where(
                UserAccount.user_id == transfer_user_id
                and UserAccount.account_id == account_id
                and UserAccount.is_active == True
            )
        )

        user_account = user_account.first()

        # Update balance
        existing_balance = await session.scalars(
            select(Balance).where(
                Balance.user_account_id == user_account.id and Balance.ccy == ccy
            )
        )
        existing_balance = existing_balance.first()

        if not existing_balance:
            existing_balance = Balance(
                user_account_id=user_account.id, balance=amount, ccy=ccy
            )
            session.add(existing_balance)
            await session.flush()
        else:
            # await session.execute(
            #     update(Balance)
            #     .where(Balance.id == existing_balance.id)
            #     .values(balance=existing_balance.balance + amount)
            # )
            existing_balance.balance += amount

        # Create history record
        history = BalanceHistory(
            balance_id=existing_balance.id,
            amount=amount,
            ccy=ccy,
            transfer_in=transfer_in,
            created_at=datetime.now(),
        )
        session.add(history)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        print(f"Transfer failed: {str(e)}")
        return False
