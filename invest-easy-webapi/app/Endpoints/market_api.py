from typing import Annotated, List
from fastapi import APIRouter, Depends
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.market_service.market_service import MarketService


router = APIRouter(
    prefix="/market",
    tags=["market"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/snapshot")
async def get_market_snapshot(
    code_list: List[str], svc: Annotated[MarketService, Depends(MarketService)]
):
    return svc.get_market_snapshot(code_list=code_list)
