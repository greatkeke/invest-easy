from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..infrastructure.users import current_active_user
from ..infrastructure.users import User
from ..services.position_service import PositionResponse, PositionService


router = APIRouter(
    prefix="/positions",
    tags=["positions"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[PositionResponse])
async def get_positions_by_user_id(
    user: User = Depends(current_active_user),
    position_service: PositionService = Depends(PositionService),
):
    try:
        positions = await position_service.get_positions_by_user_id(user.id)
        return positions
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
