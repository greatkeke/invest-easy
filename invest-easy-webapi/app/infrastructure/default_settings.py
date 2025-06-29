from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.defind_item import DefinedItem, DefinedGroup, DefinedItemType
import logging

logger = logging.getLogger(__name__)


class GroupNames:
    GENERAL = "General"
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
    general_group = await get_or_create_group(session, GroupNames.GENERAL)
    groups = {
        group.name: group
        for group in [general_group, notification_group, security_group]
    }

    # Define all default settings
    general_settings = [
        DefinedItem("Language", "English,简体中文,繁体中文", DefinedItemType.SINGLE),
        DefinedItem(
            "App mode",
            "Full mode:Features our full range of products and services, Lite mode:Features a simpler interface and easy-to-understand instructions.",
            DefinedItemType.SINGLE,
        ),
    ]
    notification_settings = [
        DefinedItem("Email Notification", "true", DefinedItemType.BOOLEAN),
        DefinedItem(
            "Email Address to receive notifications", "", DefinedItemType.EMAIL
        ),
        DefinedItem("SMS Notifications", "false", DefinedItemType.BOOLEAN),
        DefinedItem(
            "Phone number to receive SMS notifications",
            "",
            DefinedItemType.PHONE,
        ),
        DefinedItem("App Notification", "true", DefinedItemType.BOOLEAN),
        DefinedItem("Trade Information", "true", DefinedItemType.BOOLEAN),
        DefinedItem("Market Information", "true", DefinedItemType.BOOLEAN),
        DefinedItem("Order Information", "true", DefinedItemType.BOOLEAN),
        DefinedItem("Government Information", "true", DefinedItemType.BOOLEAN),
        DefinedItem("Policy Information", "true", DefinedItemType.BOOLEAN),
        DefinedItem("Environment Information", "true", DefinedItemType.BOOLEAN),
        DefinedItem(
            "Important Financial Information (CPI)",
            "true",
            DefinedItemType.BOOLEAN,
        ),
    ]
    security_settings = [
        DefinedItem(
            "Login Devices",
            "Windows, MacOS, iOS, Android",
            DefinedItemType.OPTIONS,
        ),
        DefinedItem(
            "Login Credentials",
            "PIN, FaceID, FingerPrint",
            DefinedItemType.OPTIONS,
        ),
        DefinedItem(
            "Verify Identity",
            "You're verified with HSBC accounts",
            DefinedItemType.TEXT,
            False,
        ),
    ]
    default_settings = {
        GroupNames.GENERAL: general_settings,
        GroupNames.NOTIFICATION: notification_settings,
        GroupNames.SECURITY: security_settings,
    }

    # Create or update items
    for group_name, items in default_settings.items():
        group = groups[group_name]
        for item in items:
            # Check if item exists
            existing = (
                (
                    await session.execute(
                        select(DefinedItem).where(
                            DefinedItem.group_id == group.id,
                            DefinedItem.name == item.name,
                            DefinedItem.editable == item.editable,
                            DefinedItem.secret == item.secret,
                            DefinedItem.note == item.note,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if existing:
                # Update existing item
                existing.value = item.value
                existing.type = item.type
                existing.editable = item.editable
                existing.secret = item.secret
                existing.note = item.note
                existing.updated_at = datetime.now()
            else:
                # Create new item
                new_item = DefinedItem(
                    name=item.name,
                    value=item.value,
                    type=item.type,
                    editable=item.editable if item.editable is not None else True,
                    secret=item.secret if item.secret is not None else False,
                    note=item.note,
                )
                new_item.group_id = group.id
                session.add(new_item)

    await session.commit()
    return True
