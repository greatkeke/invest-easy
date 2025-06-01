from datetime import datetime
from uuid import UUID
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
    update,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base, AsyncSession, get_async_session


class Balance(Base):
    __tablename__ = "balances"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_account_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_accounts.id"), nullable=False
    )
    balance = mapped_column(Float, nullable=False, default=0.00)
    ccy = mapped_column(String(3), nullable=False, default="HKD")
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user_account = relationship("UserAccount", back_populates="balances")


class BalanceHistory(Base):
    __tablename__ = "balance_histories"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    ccy = mapped_column(String(3), nullable=False)
    transfer_in = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)

    account = relationship("Account", back_populates="balance_histories")


async def transfer_in_amount(
    transfer_user_id: UUID_ID,
    account_id: UUID,
    amount: float,
    ccy: str,
    session: AsyncSession,
    transfer_in=True
):
    try:
        # Update balance
        existing_balance = await session.execute(
            select(Balance).where(
                Balance.user_account_id == transfer_user_id, Balance.ccy == ccy
            )
        )
        existing_balance = existing_balance.scalar_one_or_none()

        if not existing_balance:
            existing_balance = Balance(
                user_account_id=transfer_user_id, balance=amount, ccy=ccy
            )
            session.add(existing_balance)
        else:
            await session.execute(
                update(Balance)
                .where(Balance.id == existing_balance.id)
                .values(balance=existing_balance.balance + amount)
            )
            # existing_balance.balance += amount

        # Create history record
        history = BalanceHistory(
            account_id=account_id, amount=amount, ccy=ccy, transfer_in=transfer_in
        )
        session.add(history)

        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        print(f"Transfer failed: {str(e)}")
        return False
