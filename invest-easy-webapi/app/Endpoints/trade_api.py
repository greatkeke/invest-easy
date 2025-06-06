from typing import Annotated, List
from fastapi import APIRouter, Depends
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.market_service.market_service import MarketService


router = APIRouter(
    prefix="/trade",
    tags=["trade"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/positions")
async def get_positions():
    return []
