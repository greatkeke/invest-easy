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
                "editable": item.editable,
                "secret": item.secret,
                "user_defined_value": value.value if value else None,
            }
            for item, value in settings
        ]

    async def update_settings(
        self, group_name: str, settings: Dict[str, str], user_id: uuid.UUID
    ) -> bool:
        """
        Update user settings for a group.
        Creates or updates DefinedValue records for each setting.
        """
        # Get all defined items for the group
        items = await self.session.execute(
            select(DefinedItem)
            .join(DefinedGroup, DefinedItem.group_id == DefinedGroup.id)
            .where(
                DefinedGroup.name == group_name,
                DefinedGroup.is_active == True,
                DefinedItem.is_active == True,
            )
        )
        items = items.scalars().all()

        # Get existing user values
        existing_values = await self.session.execute(
            select(DefinedValue).where(
                DefinedValue.item_id.in_([item.id for item in items]),
                DefinedValue.user_id == user_id,
                DefinedValue.is_active == True,
            )
        )
        existing_values = {v.item_id: v for v in existing_values.scalars().all()}

        # Update or create values
        for item in items:
            if item.name in settings:
                value = settings[item.name]
                if item.id in existing_values:
                    # Update existing
                    existing_values[item.id].value = value
                else:
                    # Create new
                    new_value = DefinedValue(
                        item_id=item.id, user_id=user_id, value=value, is_active=True
                    )
                    self.session.add(new_value)

        await self.session.commit()
        return True
