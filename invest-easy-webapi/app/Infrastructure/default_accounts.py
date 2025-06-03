from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ..Domain.accounts import Account, UserAccount


async def create_default_account(
    user_id: uuid.UUID, username: str, ccy: str, session: AsyncSession
):
    """Create a default account for a new user"""
    # Create the account
    account = Account(
        name=f"{username} - {ccy} account", ccy=ccy, created_at=datetime.now(), updated_at=datetime.now()
    )
    session.add(account)
    await session.flush()  # Get the account ID

    # Link user to account
    user_account = UserAccount(user_id=user_id, account_id=account.id)
    session.add(user_account)
    await session.commit()

    return account
