from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.watchlist_service import WatchlistService


class WatchlistItemRequest(BaseModel):
    code: str
    tags: str | None = None
    notes: str | None = None


router = APIRouter(
    prefix="/watchlist",
    tags=["watchlist"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add")
async def add_to_watchlist(
    svc: Annotated[WatchlistService, Depends(WatchlistService)],
    user: Annotated[User, Depends(current_active_user)],
    item: WatchlistItemRequest,
):
    """
    Add an instrument to user's watchlist

    Args:
        code: Instrument code to add
        tags: Optional tags (comma separated)
        notes: Optional notes

    Returns:
        The created watchlist record
    """
    try:
        return await svc.add_to_watchlist(
            user_id=user.id, code=item.code, tags=item.tags, notes=item.notes
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/remove/{instrument_code}")
async def remove_from_watchlist(
    instrument_code: str,
    svc: Annotated[WatchlistService, Depends(WatchlistService)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Remove an instrument from user's watchlist

    Args:
        instrument_code: Instrument code to remove

    Returns:
        bool: True if removed, False if not found
    """
    try:
        return await svc.remove_from_watchlist(
            user_id=user.id, instrument_code=instrument_code
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list")
async def get_watchlist(
    svc: Annotated[WatchlistService, Depends(WatchlistService)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Get user's watchlist

    Returns:
        List of watched instruments
    """
    try:
        return await svc.get_watchlist(user_id=user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/is-watched/{instrument_code}")
async def is_watched(
    instrument_code: str,
    svc: Annotated[WatchlistService, Depends(WatchlistService)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Check if instrument is in user's watchlist

    Args:
        instrument_code: Instrument code to check

    Returns:
        bool: True if watched, False otherwise
    """
    try:
        return await svc.is_watched(user_id=user.id, instrument_code=instrument_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
