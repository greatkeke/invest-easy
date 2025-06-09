from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.market_service import MarketService
from ..services.trade_service import TradeService
from ..infrastructure.db import get_async_session


router = APIRouter(
    prefix="/trade",
    tags=["trade"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


class SubmitPositionRequest(BaseModel):
    account_id: uuid.UUID
    code: str
    price: float
    quantity: float
    stock_in: bool = True


@router.get("/positions")
async def get_positions():
    return []


@router.post("/in")
async def trade_in(
    request: SubmitPositionRequest,
    user: User = Depends(current_active_user),
    trade_service: TradeService = Depends(TradeService)
):
    try:
        order = await trade_service.trade_in(
            user_id=user.id,
            account_id=request.account_id,
            code=request.code,
            price=request.price,
            quantity=request.quantity,
            stock_in=request.stock_in
        )
        return {"success": True, "order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
