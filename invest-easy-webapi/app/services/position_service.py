import uuid
import logging
from typing import Annotated, List
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.positions import Position
from ..domain.instruments import Instrument
from ..domain.accounts import UserAccount
from ..infrastructure.db import get_async_session
from ..services.market_service import MarketService
from ..services.balance_service import BalanceService


class PositionResponse(BaseModel):
    id: uuid.UUID
    quantity: float
    price: float
    avg_price: float
    market_value: float
    pl: float
    today_pl: float
    percentage: float
    instrument_code: str
    instrument_name: str


class PositionService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        market_service: Annotated[MarketService, Depends(MarketService)],
        balance_service: Annotated[BalanceService, Depends(BalanceService)],
    ):
        self.session = session
        self.market_service = market_service
        self.balance_service = balance_service

    async def get_positions_by_user_id(self, user_id: uuid.UUID):
        try:
            # Get all active user accounts for this user
            user_accounts = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == user_id, UserAccount.is_active == True
                )
            )
            user_accounts = user_accounts.all()

            if not user_accounts:
                return []

            # Get positions for all user accounts
            positions = []
            for uaccount in user_accounts:
                account_positions = await self.session.execute(
                    select(Position, Instrument)
                    .join(Instrument, Position.instrument_id == Instrument.id)
                    .where(
                        Position.user_account_id == uaccount.id,
                        Position.quantity > 0,
                        Position.is_active == True,
                    )
                )
                # Get all positions at once and store them
                positions_data = account_positions.all()

                # Collect all instrument codes for batch market data lookup
                instrument_codes = [instrument.code for _, instrument in positions_data]
                if not instrument_codes or len(instrument_codes) < 1:
                    continue

                market_data = {
                    item["code"]: item
                    for item in self.market_service.get_market_snapshot(
                        instrument_codes
                    )
                }

                # Calculate total market value of all positions
                total_market_value = sum(
                    position.quantity * position.avg_price
                    for position, _ in positions_data
                )

                # Get account balance (handles both object and dict return types)
                balances = await self.balance_service.get_balances(
                    user_id, uaccount.account_id
                )
                if not balances or len(balances) != 1:
                    account_balance = 0.0
                else:
                    balance = balances[0]
                    if isinstance(balance, dict):
                        account_balance = balance.get("balance", 0.0)  # Dict case
                    else:
                        account_balance = balance.balance  # Object case

                # Calculate denominator for percentage (total market value + balance)
                denominator = total_market_value + account_balance

                positions.extend(
                    PositionResponse(
                        id=position.id,
                        quantity=position.quantity,
                        price=market_data[instrument.code]["last_price"],
                        avg_price=position.avg_price,
                        market_value=position.quantity * position.avg_price,
                        pl=(
                            market_data[instrument.code]["last_price"]
                            - position.avg_price
                        )
                        * position.quantity,
                        today_pl=(
                            market_data[instrument.code]["last_price"]
                            - market_data[instrument.code]["prev_close_price"]
                        )
                        * position.quantity,
                        instrument_code=instrument.code,
                        instrument_name=instrument.name,
                        percentage=(
                            (position.quantity * position.avg_price) / denominator
                            if denominator != 0
                            else 0.0
                        ),
                    ).model_dump()
                    for position, instrument in positions_data
                )

            return positions
        except Exception as e:
            logging.error(f"Failed to get positions for user {user_id}: {str(e)}")
            raise
