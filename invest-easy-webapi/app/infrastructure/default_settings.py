from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.defind_item import DefinedItem, DefinedGroup, DefinedAttributeType
import logging

logger = logging.getLogger(__name__)


class GroupNames:
    NOTIFICATION = "Notification"
    SECURITY = "Security"


async def get_or_create_group(session: AsyncSession, name: str) -> DefinedGroup:
    try:
        group = (
            (
                await session.execute(
                    select(DefinedGroup).where(DefinedGroup.name == name)
                )
            )
            .scalars()
            .first()
        )
        if not group:
            group = DefinedGroup(name=name)
            session.add(group)
            await session.flush()
        return group
    except Exception as e:
        logger.error(f"Error getting/creating group {name}: {e}")
        raise


async def predefined_settings(session: AsyncSession):
    # Get or create groups
    notification_group = await get_or_create_group(session, GroupNames.NOTIFICATION)
    security_group = await get_or_create_group(session, GroupNames.SECURITY)
    groups = {group.name: group for group in [notification_group, security_group]}

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
                "Windows, MacOS, iOS, Android",
                DefinedAttributeType.OPTIONS,
            ),
            (
                "Login Credentials",
                "PIN, FaceID, FingerPrint",
                DefinedAttributeType.OPTIONS,
            ),
            (
                "Verify Identity",
                "You're verified with HSBC accounts",
                DefinedAttributeType.TEXT,
                False
            ),
        ],
    }

    # Create or update items
    for group_name, items in default_settings.items():
        group = groups[group_name]
        for item in items:
            # Check if item exists
            editable = item[3] if len(item) > 3 else True
            secret = item[4] if len(item) > 4 else False
            existing = (
                (
                    await session.execute(
                        select(DefinedItem)
                        .where(DefinedItem.group_id == group.id)
                        .where(DefinedItem.name == item[0])
                        .where(DefinedItem.editable == editable)
                        .where(DefinedItem.secret == secret)
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
                existing.secret = secret
                existing.updated_at = datetime.now()
            else:
                # Create new item
                new_item = DefinedItem(
                    group_id=group.id,
                    name=item[0],
                    value=item[1],
                    type=item[2],
                    editable = editable,
                    secret = secret
                )
                session.add(new_item)

    await session.commit()
    return True
