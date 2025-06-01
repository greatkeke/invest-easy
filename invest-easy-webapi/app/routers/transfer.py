import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..users import User, current_active_user
from ..balance.balance import transfer_in_amount
from ..db import Base, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped


class TransferRequest(BaseModel):
    account_id: uuid.UUID
    amount: float
    ccy: str = "HKD"
    transfer_in: bool = True


router = APIRouter(
    prefix="/transfer",
    tags=["balance"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get():
    return {"transfer": 1}


@router.post("/in")
async def transfer_amount(
    request: TransferRequest,
    current_user: User = Depends(current_active_user),
    session = Depends(get_async_session)
):
    success = await transfer_in_amount(
        transfer_user_id=current_user.id,
        account_id=request.account_id,
        amount=request.amount,
        ccy=request.ccy,
        session=session
    )

    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed")

    return {"status": "success", "message": "Transfer completed"}
