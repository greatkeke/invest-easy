from datetime import datetime
from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...Domain.accounts import UserAccount
from ...Domain.balance import Balance, BalanceHistory
from ...Infrastructure.db import get_async_session


class balance_service:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session

    async def transfer_in_amount(
        self,
        transfer_user_id: uuid.UUID,
        account_id: uuid.UUID,
        amount: float,
        ccy: str,
        transfer_in=True,
    ):
        try:
            user_account = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == transfer_user_id
                    and UserAccount.account_id == account_id
                    and UserAccount.is_active == True
                )
            )

            user_account = user_account.first()

            # Update balance
            existing_balance = await self.session.scalars(
                select(Balance).where(
                    Balance.user_account_id == user_account.id and Balance.ccy == ccy  # type: ignore
                )
            )
            existing_balance = existing_balance.first()

            if not existing_balance:
                existing_balance = Balance(
                    user_account_id=user_account.id, balance=amount, ccy=ccy  # type: ignore
                )
                self.session.add(existing_balance)
                await self.session.flush()
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
            self.session.add(history)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Transfer failed: {str(e)}")
            return False
