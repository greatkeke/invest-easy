from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.defind_item import DefinedItem, DefinedGroup, DefinedAttributeType


async def create_default_settings(session: AsyncSession):
    user_id: Optional[uuid.UUID] = None #None for global settings
    """Create or update default settings for a user"""
    # Get or create groups
    notification_group = (
        (
            await session.execute(
                select(DefinedGroup).where(DefinedGroup.name == "Notification")
            )
        )
        .scalars()
        .first()
    )
    if not notification_group:
        notification_group = DefinedGroup(name="Notification")
        session.add(notification_group)

    security_group = (
        (
            await session.execute(
                select(DefinedGroup).where(DefinedGroup.name == "Security")
            )
        )
        .scalars()
        .first()
    )
    if not security_group:
        security_group = DefinedGroup(name="Security")
        session.add(security_group)

    await session.flush()

    # Define all default settings
    default_settings = {
        "Notification": [
            ("Email Notification", "true", DefinedAttributeType.BOOLEAN),
            ("Email Address to receive notifications", "", DefinedAttributeType.EMAIL),
            ("SMS Notifications", "false", DefinedAttributeType.BOOLEAN),
            (
                "Phone number to receive SMS notifications",
                "",
                DefinedAttributeType.PHONE,
            ),
            ("App Notification", "true", DefinedAttributeType.BOOLEAN),
            ("Trade Information", "true", DefinedAttributeType.BOOLEAN),
            ("Market Information", "true", DefinedAttributeType.BOOLEAN),
            ("Order Information", "true", DefinedAttributeType.BOOLEAN),
            ("Government Information", "true", DefinedAttributeType.BOOLEAN),
            ("Policy Information", "true", DefinedAttributeType.BOOLEAN),
            ("Environment Information", "true", DefinedAttributeType.BOOLEAN),
            (
                "Important Financial Information (CPI)",
                "true",
                DefinedAttributeType.BOOLEAN,
            ),
        ],
        "Security": [
            (
                "Login Devices",
                "OnePlus phone 13T, iOS 12mini, mac mini m4",
                DefinedAttributeType.OPTIONS,
            ),
            (
                "Login Credentials",
                "PIN, FaceID, FingerPrint",
                DefinedAttributeType.OPTIONS,
                False,
            ),
            (
                "Verify Identity",
                "You're verified with HSBC accounts",
                DefinedAttributeType.TEXT,
                False,
            ),
        ],
    }

    # Create or update items
    for group_name, items in default_settings.items():
        group = notification_group if group_name == "Notification" else security_group
        for item in items:
            # Handle optional editable parameter
            editable = item[3] if len(item) > 3 else True

            # Check if item exists
            existing = (
                (
                    await session.execute(
                        select(DefinedItem)
                        .where(DefinedItem.group_id == group.id)
                        .where(DefinedItem.user_id == user_id)
                        .where(DefinedItem.name == item[0])
                    )
                )
                .scalars()
                .first()
            )

            if existing:
                # Update existing item
                existing.value = item[1]
                existing.type = item[2]
                existing.editable = editable
            else:
                # Create new item
                new_item = DefinedItem(
                    group_id=group.id,
                    user_id=user_id,
                    name=item[0],
                    value=item[1],
                    type=item[2],
                    editable=editable,
                )
                session.add(new_item)

    await session.commit()
    return True
