from typing import Annotated, List
from fastapi import APIRouter, Depends
from ..Infrastructure.users import current_active_user
from ..Infrastructure.users import User
from ..Services.market_service.market_service import market_service


router = APIRouter(
    prefix="/trade",
    tags=["trade"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/positions")
async def get_positions():
    return []


@router.post("/market/snapshot")
async def get_market_snapshot(
    code_list: List[str], svc: Annotated[market_service, Depends(market_service)]
):
    return svc.get_market_snapshot(code_list=code_list)
