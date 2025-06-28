from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from ..domain.users import User
from ..infrastructure.users import current_active_user
from ..services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/defined-items/{group_name}")
async def get_defined_items(
    group_name: str,
    user: User = Depends(current_active_user),
    setting_svc: SettingsService = Depends(SettingsService),
) -> List[Dict[str, Any]]:
    """
    Get defined items for a group.
    """
    items = await setting_svc.get_defined_items(group_name, user.id)
    return items
