from datetime import datetime
import logging
from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...Domain.accounts import UserAccount, Account
from ...Domain.balance import Balance, BalanceHistory
from ...Infrastructure.db import get_async_session
from ...Domain.users import User


class balance_service:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session

    async def transfer_in_amount(
        self,
        transfer_user_id: uuid.UUID,
        account_id: uuid.UUID,
        amount: float,
        transfer_in=True,
    ):
        try:
            user_account = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == transfer_user_id,
                    UserAccount.account_id == account_id,
                    UserAccount.is_active == True,
                )
            )

            user_account = user_account.first()

            if not user_account:
                logging.error(
                    f"No user account found with: user_id:{transfer_user_id}, account_id: {account_id}."
                )
                raise ValueError("No user account found.")

            account = await self.session.scalars(
                select(Account).where(
                    Account.id == account_id, Account.is_active == True
                )
            )

            account = account.first()

            if not account:
                logging.error(f"No account found by: {account_id}.")
                raise ValueError("No account found.")

            # Update balance
            existing_balance = await self.session.scalars(
                select(Balance).where(
                    Balance.user_account_id == user_account.id,
                    Balance.ccy == account.ccy,
                )
            )
            existing_balance = existing_balance.first()

            if not existing_balance:
                existing_balance = Balance(
                    user_account_id=user_account.id, balance=0.0, ccy=account.ccy
                )
                self.session.add(existing_balance)
                await self.session.flush()

            if transfer_in:
                existing_balance.balance += amount
            else:
                if existing_balance.balance >= amount:
                    existing_balance.balance -= amount
                else:
                    raise ValueError("No such amount balance left.")

            # Create history record
            history = BalanceHistory(
                balance_id=existing_balance.id,
                amount=amount,
                ccy=account.ccy,
                transfer_in=transfer_in,
                created_at=datetime.now(),
            )
            self.session.add(history)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Transfer failed: {str(e)}")
            return False

    async def get_records(
        self, user_id: uuid.UUID, pageSize: int = 3, pageIndex: int = 0
    ):
        records = await self.session.execute(
            select(BalanceHistory, Account.name)
            .join(Balance, BalanceHistory.balance_id == Balance.id)
            .join(UserAccount, UserAccount.id == Balance.user_account_id)
            .join(Account, Account.id == UserAccount.account_id)
            .where(UserAccount.user_id == user_id, UserAccount.is_active == True)
            .order_by(BalanceHistory.created_at.desc())
            .limit(pageSize)
            .offset(pageIndex * pageSize)
        )
        return [
            {"record": record[0], "account_name": record[1]} for record in records.all()
        ]
