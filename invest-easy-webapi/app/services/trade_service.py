import uuid
import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.positions import Position
from ..domain.orders import Order, OrderStatus
from ..domain.instruments import Instrument
from ..domain.accounts import UserAccount
from ..services.balance_service import BalanceService, BalanceType
from ..services.market_service import MarketService
from ..infrastructure.db import get_async_session


class TradeService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        market_service: Annotated[MarketService, Depends(MarketService)],
        balance_service: Annotated[BalanceService, Depends(BalanceService)],
    ):
        self.session = session
        self.balance_service = balance_service
        self.market_service = market_service

    async def trade_in(
        self,
        user_id: uuid.UUID,
        account_id: uuid.UUID,
        code: str,
        price: float,
        quantity: float,
    ):
        try:
            # Get UserAccount
            user_account = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == user_id,
                    UserAccount.account_id == account_id,
                    UserAccount.is_active == True,
                )
            )
            user_account = user_account.first()
            if not user_account:
                raise ValueError("User account not found")

            # Get Instrument
            instrument = await self.session.scalars(
                select(Instrument).where(
                    Instrument.code == code, Instrument.is_active == True
                )
            )
            instrument = instrument.first()

            if not instrument:
                raise ValueError(f"No such instrument found: {code}")

            # Get or create Position
            position = await self.session.scalars(
                select(Position).where(
                    Position.instrument_id == instrument.id,
                    Position.user_account_id == user_account.id,
                    Position.is_active == True,
                )
            )
            position = position.first()

            if not position:
                position = Position(
                    instrument_id=instrument.id,
                    user_account_id=user_account.id,
                    quantity=0,
                    avg_price=0,
                )
                self.session.add(position)
                await self.session.flush()

            # Calculate new avg_price
            new_avg_price = (
                position.quantity * position.avg_price + quantity * price
            ) / (position.quantity + quantity)
            position.avg_price = new_avg_price
            position.quantity += quantity
            await self.session.flush()

            # Create Order
            order = Order(
                instrument_id=instrument.id,
                user_account_id=user_account.id,
                price=price,
                quantity=quantity,
                trade_in=True,
                status=OrderStatus.FILLED,
                position_id=position.id,
            )
            self.session.add(order)

            # Transfer amount
            transfer_success = await self.balance_service.transfer_in_amount(
                user_id, account_id, price * quantity, BalanceType.TRADE_BUY
            )
            if not transfer_success:
                raise ValueError("Balance transfer failed")

            await self.session.commit()
            return order
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Submit position failed: {str(e)}")
            raise

    async def trade_out(
        self,
        user_id: uuid.UUID,
        account_id: uuid.UUID,
        code: str,
        price: float,
        quantity: float,
    ):
        try:
            # Get UserAccount
            user_account = await self.session.scalars(
                select(UserAccount).where(
                    UserAccount.user_id == user_id,
                    UserAccount.account_id == account_id,
                    UserAccount.is_active == True,
                )
            )
            user_account = user_account.first()
            if not user_account:
                raise ValueError("User account not found")

            # Get Instrument
            instrument = await self.session.scalars(
                select(Instrument).where(
                    Instrument.code == code, Instrument.is_active == True
                )
            )
            instrument = instrument.first()
            if not instrument:
                raise ValueError(f"No such instrument found: {code}")

            # Get Position
            position = await self.session.scalars(
                select(Position).where(
                    Position.instrument_id == instrument.id,
                    Position.user_account_id == user_account.id,
                    Position.is_active == True,
                )
            )
            position = position.first()
            if not position:
                raise ValueError("Position not found")
            if position.quantity < quantity:
                raise ValueError("Insufficient position quantity")

            # Calculate new avg_price
            if position.quantity <= quantity:
                new_avg_price = 0.0
            else:
                new_avg_price = (
                    position.quantity * position.avg_price - quantity * price
                ) / (position.quantity - quantity)
            position.avg_price = new_avg_price
            position.quantity -= quantity
            await self.session.flush()

            # Create Order
            order = Order(
                instrument_id=instrument.id,
                user_account_id=user_account.id,
                price=price,
                quantity=quantity,
                trade_in=False,
                status=OrderStatus.FILLED,
                position_id=position.id,
            )
            self.session.add(order)

            # Transfer amount out
            transfer_success = await self.balance_service.transfer_in_amount(
                user_id, account_id, price * quantity, BalanceType.TRADE_SELL
            )
            if not transfer_success:
                raise ValueError("Balance transfer failed")

            await self.session.commit()
            return order
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Trade out failed: {str(e)}")
            raise
