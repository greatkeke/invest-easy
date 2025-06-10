import uuid
import logging
from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.positions import Position
from ..domain.instruments import Instrument
from ..domain.accounts import UserAccount
from ..infrastructure.db import get_async_session


class PositionResponse(BaseModel):
    id: uuid.UUID
    quantity: float
    avg_price: float 
    instrument_code: str
    instrument_name: str


class PositionService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
        self.session = session

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
                positions.extend(
                    PositionResponse(
                        id=position.id,
                        quantity=position.quantity,
                        avg_price=position.avg_price,
                        instrument_code=instrument.code,
                        instrument_name=instrument.name,
                    ).model_dump()
                    for position, instrument in account_positions.all()
                )

            return positions
        except Exception as e:
            logging.error(f"Failed to get positions for user {user_id}: {str(e)}")
            raise
