from datetime import datetime
import logging
from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.accounts import UserAccount, Account
from ..domain.balance import Balance, BalanceHistory, BalanceType
from ..infrastructure.db import get_async_session
from ..infrastructure.fxrate_service import FxRateService


class BalanceService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        fxSvc: Annotated[FxRateService, Depends(FxRateService)],
    ):
        self.session = session
        self.fxSvc = fxSvc

    async def transfer_in_amount(
        self,
        transfer_user_id: uuid.UUID,
        account_id: uuid.UUID,
        amount: float,
        type: BalanceType = BalanceType.TRANSFER_IN,
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

            # overview balance
            overview_balance = await self.session.scalars(
                select(Balance)
                .join(UserAccount, UserAccount.id == Balance.user_account_id)
                .join(Account, UserAccount.account_id == Account.id)
                .where(
                    Account.is_overview == True,
                    Account.is_active == True,
                    UserAccount.user_id == transfer_user_id,
                    UserAccount.is_active == True,
                    Balance.is_overview == True,
                    Balance.is_active == True,
                )
            )
            overview_balance = overview_balance.first()
            if not overview_balance:
                raise ValueError("No overview account/balance found")
            
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

            is_increment = type in [BalanceType.TRANSFER_IN, BalanceType.TRADE_SELL]

            base_fxrate = self.fxSvc.get_fxrate_by_ccy(existing_balance.ccy)
            converted_amount = amount * base_fxrate

            if is_increment:
                existing_balance.balance += amount
                overview_balance.balance += converted_amount
            else:
                if existing_balance.balance >= amount:
                    existing_balance.balance -= amount
                    overview_balance.balance -= converted_amount
                else:
                    raise ValueError("No such amount balance left.")

            # Create history record
            history = BalanceHistory(
                balance_id=existing_balance.id,
                amount=amount,
                ccy=account.ccy,
                type=type,
                is_increment=is_increment,
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

    async def get_balances(
        self, user_id: uuid.UUID, account_id: uuid.UUID | None = None
    ):
        if account_id:
            # Get specific account balance
            user_account = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == user_id,
                    UserAccount.account_id == account_id,
                    UserAccount.is_active == True,
                )
            )
            user_account = user_account.first()
            if not user_account:
                return []

            balances = await self.session.scalars(
                select(Balance).where(
                    Balance.user_account_id == user_account.id,
                    Balance.is_active == True,
                )
            )
            return [balance.__dict__ for balance in balances.all()]
        else:
            # Batch fetch all accounts and balances for user
            user_accounts = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == user_id, UserAccount.is_active == True
                )
            )
            user_accounts = user_accounts.all()
            if not user_accounts:
                return []

            # Get all balances for these accounts in one query
            account_ids = [ua.id for ua in user_accounts]
            balances = await self.session.scalars(
                select(Balance).where(Balance.user_account_id.in_(account_ids))
            )

            # Return flattened list of all balances
            return balances.all()
