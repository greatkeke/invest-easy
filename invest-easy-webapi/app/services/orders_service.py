import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from fastapi import Depends
from sqlalchemy import select, desc
from ..domain.accounts import UserAccount
from ..domain.instruments import Instrument
from ..domain.orders import Order
from ..infrastructure.db import get_async_session


class OrdersService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session

    async def get_user_orders(
        self, user_id: uuid.UUID, page: int = 1, page_size: int = 5
    ) -> List[dict]:
        # Get paginated results
        result = await self.session.execute(
            select(Order, Instrument)
            .join(UserAccount, Order.user_account_id == UserAccount.id)
            .join(Instrument, Order.instrument_id == Instrument.id)
            .where(
                UserAccount.user_id == user_id,
                UserAccount.is_active == True,
                Instrument.is_active == True,
                Order.is_active == True,
            )
            .order_by(desc(Order.created_at))
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        return [
            {
                "order": {
                    "id": order.id,
                    "user_account_id": order.user_account_id,
                    "instrument_id": order.instrument_id,
                    "position_id": order.position_id,
                    "quantity": order.quantity,
                    "price": order.price,
                    "trade_in": order.trade_in,
                    "status": order.status.name,
                    "created_at": order.created_at,
                },
                "instrument": instrument,
            }
            for order, instrument in result.all()
        ]
