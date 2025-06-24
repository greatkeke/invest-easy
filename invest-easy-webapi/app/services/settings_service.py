from typing import List, Dict, Any, Optional
import uuid
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..domain.defind_item import DefinedItem, DefinedGroup
from ..infrastructure.db import get_async_session


class SettingsService:
    def __init__(self, db: AsyncSession = Depends(get_async_session)) -> None:
        self.session = db

    async def get_defined_items(
        self, group_name: str, user_id: Optional[uuid.UUID] = None
    ) -> List[Dict[str, Any]]:
        """
        Get defined items for a group, combining global and user-specific settings.
        User-specific settings override global settings.
        """
        # First get the group_id from group_name
        group = (
            (
                await self.session.execute(
                    select(DefinedGroup).where(DefinedGroup.name == group_name)
                )
            )
            .scalars()
            .first()
        )
        if not group:
            return []

        # Get global settings (user_id=None)
        global_items = (
            (
                await self.session.execute(
                    select(DefinedItem).where(
                        DefinedItem.group_id == group.id, DefinedItem.user_id == None
                    )
                )
            )
            .scalars()
            .all()
        )

        # Get user-specific settings if user_id provided
        user_items = []
        if user_id:
            user_items = (
                (
                    await self.session.execute(
                        select(DefinedItem).where(
                            DefinedItem.group_id == group.id,
                            DefinedItem.user_id == user_id,
                        )
                    )
                )
                .scalars()
                .all()
            )

        # Combine results - user items override global items
        result: Dict[str, Dict[str, Any]] = {}
        for item in global_items:
            result[item.name] = {
                "value": item.value,
                "type": item.type.name,
                "editable": item.editable,
                "secret": item.secret,
            }

        for item in user_items:
            result[item.name] = {
                "value": item.value,
                "type": item.type.name,
                "editable": item.editable,
                "secret": item.secret,
            }

        return [{"name": k, **v} for k, v in result.items()]
