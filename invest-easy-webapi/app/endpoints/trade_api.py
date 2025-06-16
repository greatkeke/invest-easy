from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.trade_service import TradeService


router = APIRouter(
    prefix="/trade",
    tags=["trade"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


class TradeRequest(BaseModel):
    account_id: uuid.UUID
    code: str
    price: float
    quantity: float


@router.post("/in")
async def trade_in(
    request: TradeRequest,
    user: User = Depends(current_active_user),
    trade_service: TradeService = Depends(TradeService),
):
    try:
        order = await trade_service.trade_in(
            user_id=user.id,
            account_id=request.account_id,
            code=request.code,
            price=request.price,
            quantity=request.quantity,
        )
        return {"success": True, "order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/out")
async def trade_out(
    request: TradeRequest,
    user: User = Depends(current_active_user),
    trade_service: TradeService = Depends(TradeService),
):
    try:
        order = await trade_service.trade_out(
            user_id=user.id,
            account_id=request.account_id,
            code=request.code,
            price=request.price,
            quantity=request.quantity,
        )
        return {"success": True, "order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
