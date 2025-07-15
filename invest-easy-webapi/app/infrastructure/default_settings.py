from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.defind_item import DefinedItem, DefinedGroup, DefinedItemType
import logging

logger = logging.getLogger(__name__)


class GroupNames:
    GENERAL = "General"
    CONTACT_DETAILS = "Contact details"
    NOTIFICATION = "Notification"
    SECURITY = "Security"
    PAY_TRANSFER = "Pay and transfer"
    COMMUNICATION_PREFERENCES = "Communication preferences"
    INVESTMENT = "Investment"
    OPEN_BANKING_CONSENT = "Open Banking consent"
    ACTIVITY_LOG = "Activity log"


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
    general_group = await get_or_create_group(session, GroupNames.GENERAL)
    contact_details_group = await get_or_create_group(
        session, GroupNames.CONTACT_DETAILS
    )
    notification_group = await get_or_create_group(session, GroupNames.NOTIFICATION)
    security_group = await get_or_create_group(session, GroupNames.SECURITY)
    payTransfer_group = await get_or_create_group(session, GroupNames.PAY_TRANSFER)
    communication_preferences_group = await get_or_create_group(
        session, GroupNames.COMMUNICATION_PREFERENCES
    )
    investment_group = await get_or_create_group(session, GroupNames.INVESTMENT)
    open_banking_consent_group = await get_or_create_group(
        session, GroupNames.OPEN_BANKING_CONSENT
    )
    activity_log_group = await get_or_create_group(session, GroupNames.ACTIVITY_LOG)

    # Define all default settings
    general_settings = [
        DefinedItem(
            "Language",
            "English,简体中文,繁体中文",
            DefinedItemType.SINGLE,
        ),
        DefinedItem(
            "App mode",
            "Full mode, Lite mode",
            DefinedItemType.SINGLE,
            note="Features our full range of products and services, Features a simpler interface and easy-to-understand instructions.",
        ),
    ]
    contact_details_settings = [
        DefinedItem(
            "Mobile number",
            "",
            DefinedItemType.PHONE,
            note="Your updated contact details will be applied to all of your accounts including any either-to-sign joint accounts.",
        ),
        DefinedItem(
            "Address",
            "",
            DefinedItemType.ADDRESS,
            note="You'll receive SMS and email notifications shortly after the update. Please contact us if you don't receive them",
        ),
        DefinedItem(
            "Email address",
            "",
            DefinedItemType.EMAIL,
            note="FPS registrations with your old mobile number and email address will cease in 1 working day. Please register again for FPS with your new contact details via mobile or online banking.",
        ),
    ]
    notification_settings = [
        DefinedItem("Email Notification", "true", DefinedItemType.BOOLEAN),
        DefinedItem(
            "Email Address to receive notifications",
            "",
            DefinedItemType.EMAIL,
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
        DefinedItem(
            "Government Information",
            "true",
            DefinedItemType.BOOLEAN,
        ),
        DefinedItem("Policy Information", "true", DefinedItemType.BOOLEAN),
        DefinedItem(
            "Environment Information",
            "true",
            DefinedItemType.BOOLEAN,
        ),
        DefinedItem(
            "Important Financial Information (CPI)",
            "true",
            DefinedItemType.BOOLEAN,
        ),
    ]
    security_settings = [
        DefinedItem(
            "Login Devices",
            "{\"Windows\":false, \"MacOS\":false, \"iOS\":false, \"Android\":false}",
            DefinedItemType.OPTIONS,
        ),
        DefinedItem(
            "Login Credentials",
            "{\"PIN\":false, \"FaceID\":false, \"FingerPrint\":false}",
            DefinedItemType.OPTIONS,
        ),
        DefinedItem(
            "Verify Identity",
            "You're verified with HSBC accounts",
            DefinedItemType.TEXT,
            False,
        ),
    ]
    payTransfer_settings = [
        DefinedItem("Transfer limits to payees", "", DefinedItemType.Empty, False),
        DefinedItem("Registered account", "50000.00", DefinedItemType.NUMBER),
        DefinedItem("Non-registered payee", "40000.00", DefinedItemType.NUMBER),
        DefinedItem("Other transfer limits", "", DefinedItemType.Empty, editable=False),
        DefinedItem("Small-value payments", "10000.00", DefinedItemType.NUMBER),
        DefinedItem("Bill payments", "5000000.00", DefinedItemType.NUMBER),
        DefinedItem("Cross-border transfers", "1000000.00", DefinedItemType.NUMBER),
        DefinedItem("Your local HSBC account", "999999999.00", DefinedItemType.NUMBER),
        DefinedItem(
            "Reminder",
            "",
            DefinedItemType.Empty,
            editable=False,
            note="Review your transfer limits regularly and make necessary adjustments that suit your needs.\nIf you want to increase your transfer limits, we may ask for the identification number you use to bank with us to verify your identity.",
        ),
    ]
    communication_preferences_settings = [
        DefinedItem("Push notification preferences", "true", DefinedItemType.BOOLEAN),
        DefinedItem("Marketing prefernces", "true", DefinedItemType.BOOLEAN),
        DefinedItem(
            "Important notifications prefernces", "true", DefinedItemType.BOOLEAN
        ),
        DefinedItem(
            "Credit card transaction notifications",
            "true",
            DefinedItemType.BOOLEAN,
            note="Online, phone, fax, mail and in-app purchases up to HKD500.",
        ),
    ]
    investment_settings = [
        DefinedItem(
            "Your risk profile",
            "0,1,2,3,4,5",
            DefinedItemType.SINGLE,
            note="A risk profile will help you understand your risk appetite, and provide some indication of the risk tolerance for a typical investor displaying your personal investment characteristics.",
        ),
        DefinedItem(
            "Risk tips",
            "",
            DefinedItemType.Empty,
            note="On a scale of 0 to 5, the greater the number, the higher the risk you're comfortable to take.",
        ),
    ]
    open_banking_consent_settings = [
        DefinedItem(
            "",
            "",
            DefinedItemType.Empty,
            note="You can manage your consents for account data sharing between HSBC and other banks using the Open Banking service.",
        ),
        DefinedItem(
            "Data from other banks",
            "No data sharing",
            DefinedItemType.OPTIONS,
            editable=False,
            note="Here you'll see the list of consents you've provided to HSBC. This allows us to access your account data and display it on your homepage.",
        ),
    ]
    activity_log_settings = [
        DefinedItem(
            "",
            "",
            DefinedItemType.Empty,
            note="Here you'll see activities completed on HSBC Online and Mobile Banking, Rewards+ and Easy Invest in the last 90 days. This helps you to monitor your account for unauthorised access.",
        ),
        DefinedItem(
            "Warning activities",
            "",
            DefinedItemType.Empty,
            editable=False,
            note="If you don't recoginise any of the activities, please contact us immediately via Chat with us.",
        ),
    ]
    default_settings = {
        general_group: general_settings,
        contact_details_group: contact_details_settings,
        notification_group: notification_settings,
        security_group: security_settings,
        payTransfer_group: payTransfer_settings,
        communication_preferences_group: communication_preferences_settings,
        investment_group: investment_settings,
        open_banking_consent_group: open_banking_consent_settings,
        activity_log_group: activity_log_settings,
    }

    # Create or update items
    for group, items in default_settings.items():
        for item in items:
            # Check if item exists
            existing = (
                (
                    await session.execute(
                        select(DefinedItem).where(
                            DefinedItem.group_id == group.id,
                            DefinedItem.name == item.name,
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
