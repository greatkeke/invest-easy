from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.exchange_service import ExchangeService


router = APIRouter(
    prefix="/exchange",
    tags=["exchange"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


class ExchangeRequest(BaseModel):
    from_account_id: uuid.UUID
    to_account_id: uuid.UUID
    amount: float


@router.post("/")
async def exchange(
    request: ExchangeRequest,
    user: User = Depends(current_active_user),
    exchange_service: ExchangeService = Depends(ExchangeService),
):
    try:
        success = await exchange_service.exchange(
            user_id=user.id,
            from_account_id=request.from_account_id,
            to_account_id=request.to_account_id,
            amount=request.amount,
        )
        return {"success": success}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
