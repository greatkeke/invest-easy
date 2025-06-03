from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..Infrastructure.users import User, current_active_user
from ..Services.balance_service.balance_service import balance_service


class TransferRequest(BaseModel):
    account_id: uuid.UUID
    amount: float
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
    current_user: Annotated[User,  Depends(current_active_user)],
    svc: Annotated[balance_service, Depends(balance_service)],
):
    success = await svc.transfer_in_amount(
        transfer_user_id=current_user.id,
        account_id=request.account_id,
        amount=request.amount,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed")

    return {"status": "success", "message": "Transfer completed"}
