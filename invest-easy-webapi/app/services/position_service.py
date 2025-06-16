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


class PositionResponse(BaseModel):
    id: uuid.UUID
    quantity: float
    price: float
    avg_price: float
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
    ):
        self.session = session
        self.market_service = market_service

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

                positions.extend(
                    PositionResponse(
                        id=position.id,
                        quantity=position.quantity,
                        price=market_data[instrument.code]["last_price"],
                        avg_price=position.avg_price,
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
                        percentage=0.0,
                    ).model_dump()
                    for position, instrument in positions_data
                )

            return positions
        except Exception as e:
            logging.error(f"Failed to get positions for user {user_id}: {str(e)}")
            raise
