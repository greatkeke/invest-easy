from typing import List, Dict, Any, Optional
import uuid
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ..domain.defind_item import DefinedItem, DefinedGroup, DefinedValue
from ..infrastructure.db import get_async_session


class SettingsService:
    def __init__(self, db: AsyncSession = Depends(get_async_session)) -> None:
        self.session = db

    async def get_defined_items(
        self, group_name: str, user_id: uuid.UUID
    ) -> List[Dict[str, Any]]:
        """
        Get defined items for a group, combining global and user-specific settings.
        """
        settings = await self.session.execute(
            select(DefinedItem, DefinedValue)
            .join(DefinedGroup, DefinedItem.group_id == DefinedGroup.id)
            .outerjoin(
                DefinedValue,
                and_(
                    DefinedItem.id == DefinedValue.item_id,
                    DefinedValue.user_id == user_id,
                    DefinedValue.is_active == True,
                ),
            )
            .where(
                DefinedGroup.name == group_name,
                DefinedGroup.is_active == True,
                DefinedItem.is_active == True,
            )
        )
        settings = settings.all()

        return [
            {
                "item_id": item.id,
                "name": item.name,
                "item_value": item.value,
                "type": item.type.name,
                "user_defined_value": value.value if value else None,
                "editable": value.editable if value else True,
                "secret": value.secret if value else False,
            }
            for item, value in settings
        ]
