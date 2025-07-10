from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from sqlalchemy import select, and_
from ..domain.users import User
from ..domain.accounts import Account, UserAccount
from ..domain.balance import Balance
from ..infrastructure.db import get_async_session


class AccountService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session

    async def get_user_accounts(self, user: User):
        result = await self.session.execute(
            select(Account)
            .join(UserAccount, UserAccount.account_id == Account.id)
            .where(
                UserAccount.user_id == user.id,
                UserAccount.is_active == True,
                Account.is_overview == False,
                Account.is_active == True,
            )
        )
        return [
            {"id": account.id, "name": account.name, "ccy": account.ccy}
            for account in result.scalars().all()
        ]

    async def get_user_accounts_balances(self, user: User, is_overview: bool = False):
        # Get accounts
        result = await self.session.execute(
            select(Account, Balance)
            .outerjoin(
                UserAccount,
                UserAccount.account_id == Account.id,
            )
            .outerjoin(
                Balance,
                Balance.user_account_id == UserAccount.id,
            )
            .where(
                UserAccount.user_id == user.id,
                UserAccount.is_active == True,
                Account.is_overview == is_overview,
                Account.is_active == True,
                Balance.is_overview == is_overview,
                Balance.is_active == True,
            )
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
