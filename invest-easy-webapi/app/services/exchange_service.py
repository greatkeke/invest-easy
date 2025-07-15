import uuid
import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.accounts import UserAccount,Account
from ..services.balance_service import BalanceService, BalanceType
from ..infrastructure.fxrate_service import FxRateService
from ..infrastructure.db import get_async_session


class ExchangeService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        balance_service: Annotated[BalanceService, Depends(BalanceService)],
        fxrate_service: Annotated[FxRateService, Depends(FxRateService)],
    ):
        self.session = session
        self.balance_service = balance_service
        self.fxrate_service = fxrate_service

    async def exchange(
        self,
        user_id: uuid.UUID,
        from_account_id: uuid.UUID,
        to_account_id: uuid.UUID,
        amount: float,
    ):
        try:
            # Validate both accounts exist
            from_account = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == user_id,
                    UserAccount.account_id == from_account_id,
                    UserAccount.is_active == True,
                )
            )
            from_account = from_account.first()
            if not from_account:
                raise ValueError("From account not found")

            to_account = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == user_id,
                    UserAccount.account_id == to_account_id,
                    UserAccount.is_active == True,
                )
            )
            to_account = to_account.first()
            if not to_account:
                raise ValueError("To account not found")

            # Get account currencies
            from_acc = await self.session.scalar(
                select(Account).where(Account.id == from_account_id)
            )
            to_acc = await self.session.scalar(
                select(Account).where(Account.id == to_account_id)
            )
            
            if not from_acc or not to_acc:
                raise ValueError("Account details not found")

            # Get exchange rates
            from_rate = self.fxrate_service.get_fxrate_by_ccy(from_acc.ccy)
            to_rate = self.fxrate_service.get_fxrate_by_ccy(to_acc.ccy)
            
            # Calculate converted amount
            converted_amount = (from_rate / to_rate) * amount

            # Transfer amount between accounts
            transfer_out = await self.balance_service.transfer_in_amount(
                user_id, from_account_id, amount, BalanceType.TRANSFER_OUT
            )
            if not transfer_out:
                raise ValueError("Transfer out failed")

            transfer_in = await self.balance_service.transfer_in_amount(
                user_id, to_account_id, converted_amount, BalanceType.TRANSFER_IN
            )
            if not transfer_in:
                raise ValueError("Transfer in failed")

            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Exchange failed: {str(e)}")
            raise
