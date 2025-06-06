from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..domain.users import User
from ..infrastructure.users import (
    current_active_user,
    UserManager,
    get_user_manager,
)
from ..services.balance_service.balance_service import BalanceService


class TransferRequest(BaseModel):
    account_id: uuid.UUID
    amount: float
    transfer_in: bool = True
    password: str = ""


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
    current_user: Annotated[User, Depends(current_active_user)],
    svc: Annotated[BalanceService, Depends(BalanceService)],
):
    success = await svc.transfer_in_amount(
        transfer_user_id=current_user.id,
        account_id=request.account_id,
        amount=request.amount,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed")

    return {"status": success, "message": "Transfer completed"}


@router.post("/out")
async def transfer_out_amount(
    request: TransferRequest,
    current_user: Annotated[User, Depends(current_active_user)],
    svc: Annotated[BalanceService, Depends(BalanceService)],
    user_manager: Annotated[UserManager, Depends(get_user_manager)],
):
    # Verify password
    verified, update_hash = user_manager.password_helper.verify_and_update(
        request.password, current_user.hashed_password
    )
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid password")

    # Verify amount is negative
    if request.amount <= 0:
        raise HTTPException(
            status_code=400, detail="Transfer out amount must be great than 0."
        )

    success = await svc.transfer_in_amount(
        transfer_user_id=current_user.id,
        account_id=request.account_id,
        amount=request.amount,
        transfer_in=False,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed")

    return {"status": success, "message": "Transfer completed"}


@router.get("/records")
async def get_records(
    current_user: Annotated[User, Depends(current_active_user)],
    svc: Annotated[BalanceService, Depends(BalanceService)],
    pageSize: int = 3,
    pageIndex: int = 0,
):
    records = await svc.get_records(current_user.id, pageSize, pageIndex)
    return {
        "records": [
            {**record["record"].__dict__, "account_name": record["account_name"]}
            for record in records
        ],
        "pagination": {"pageSize": pageSize, "pageIndex": pageIndex},
    }
