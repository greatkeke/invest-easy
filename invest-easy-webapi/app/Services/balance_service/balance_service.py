from datetime import datetime
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...Domain.accounts import UserAccount
from ...Domain.balance import Balance, BalanceHistory


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
                Balance.user_account_id == user_account.id and Balance.ccy == ccy  # type: ignore
            )
        )
        existing_balance = existing_balance.first()

        if not existing_balance:
            existing_balance = Balance(
                user_account_id=user_account.id, balance=amount, ccy=ccy  # type: ignore
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
