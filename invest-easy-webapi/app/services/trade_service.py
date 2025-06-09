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
    ):
        self.session = session
        self.balance_service = BalanceService(session)
        self.market_service = market_service

    async def trade_in(
        self,
        user_id: uuid.UUID,
        account_id: uuid.UUID,
        code: str,
        price: float,
        amount: float,
        stock_in: bool = True,
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

            # Get or create Instrument
            instrument = await self.session.scalars(
                select(Instrument).where(Instrument.code == code, Instrument.is_active == True)
            )
            instrument = instrument.first()

            if not instrument:
                # Get market data to create instrument
                market_data = self.market_service.get_market_snapshot([code])
                if not market_data or market_data.__len__() <= 0:
                    raise ValueError(f"No such instrument found: {code}")
                else:
                    instrument = Instrument(name=market_data[0]["name"], code=code)
                self.session.add(instrument)
                await self.session.flush()

            # Get or create Position
            position = await self.session.scalars(
                select(Position).where(
                    Position.instrument_id == instrument.id,
                    Position.user_account_id == user_account.id,
                    Position.is_active == True
                )
            )
            position = position.first()
            
            if not position:
                position = Position(
                    instrument_id=instrument.id,
                    user_account_id=user_account.id,
                    amount=0,
                    avg_price=0
                )
                self.session.add(position)
                await self.session.flush()

            # Calculate new avg_price
            new_avg_price = (
                (position.amount * position.avg_price + amount * price) / 
                (position.amount + amount)
            )
            position.avg_price = new_avg_price
            position.amount += amount
            await self.session.flush()


            # Create Order
            order = Order(
                instrument_id=instrument.id,
                user_account_id=user_account.id,
                price=price,
                amount=amount,
                trade_in=stock_in,
                status=OrderStatus.FILLED,
                position_id=position.id
            )
            self.session.add(order)

            # Transfer amount
            transfer_type = (
                BalanceType.TRADE_BUY if stock_in else BalanceType.TRADE_SELL
            )
            transfer_success = await self.balance_service.transfer_in_amount(
                user_id, account_id, price * amount, transfer_type
            )
            if not transfer_success:
                raise ValueError("Balance transfer failed")

            await self.session.commit()
            return order
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Submit position failed: {str(e)}")
            raise
