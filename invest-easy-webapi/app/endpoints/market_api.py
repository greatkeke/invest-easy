from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.market_service import MarketService


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


@router.get("/rt-data")
async def get_rt_data(
    svc: Annotated[MarketService, Depends(MarketService)],
    code: str = Query(..., description="Stock code (e.g. 'HK.00700')"),
):
    """
    Get real-time tick data for a stock

    Args:
        code: Stock code (e.g. 'HK.00700')

    Returns:
        List of dicts containing real-time tick data
    """
    return svc.get_rt_data(code=code)


@router.get("/search")
async def search_stocks(
    svc: Annotated[MarketService, Depends(MarketService)],
    query: str = Query(..., description="Stock name or code to search for"),
    market: str = Query("HK", description="Market to search in (default: 'HK')"),
):
    """
    Search stocks by name or code

    Args:
        query: Stock name or code to search for
        market: Market to search in (default: 'HK')

    Returns:
        List of dicts containing matching stocks
    """
    return svc.search_stocks(query=query, market=market)
