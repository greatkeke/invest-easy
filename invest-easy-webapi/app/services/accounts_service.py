from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from sqlalchemy import select, and_
from ..domain.users import User
from ..domain.accounts import Account, UserAccount
from ..domain.balance import Balance
from sqlalchemy import select
from ..infrastructure.db import get_async_session


class AccountService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session

    async def get_user_accounts(self, user: User):
        result = await self.session.execute(
            select(Account.id, Account.name)
            .join(UserAccount, UserAccount.account_id == Account.id)
            .where(
                UserAccount.user_id == user.id,
                UserAccount.is_active == True,
                Account.is_virtual == False,
                Account.is_active == True,
            )
        )
        return [{"id": str(row[0]), "name": row[1]} for row in result.all()]

    async def get_user_accounts_balances(self, user: User):
        # Get accounts
        result = await self.session.execute(
            select(Account, Balance)
            .outerjoin(
                UserAccount,
                and_(
                    UserAccount.account_id == Account.id,
                    UserAccount.user_id == user.id,
                    UserAccount.is_active == True,
                ),
            )
            .outerjoin(
                Balance,
                and_(
                    Balance.user_account_id == UserAccount.id, Balance.is_active == True
                ),
            )
            .where(Account.is_virtual == False, Account.is_active == True)
        )
        accounts = [
            {
                "id": account.id,
                "name": account.name,
                "balance_id": balance.id if balance else None,
                "balance": balance.balance if balance else None,
                "ccy": balance.ccy if balance else None,
            }
            for account, balance in result.all()
        ]

        return accounts
