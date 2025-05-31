import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from .accounts import Account, UserAccount

async def create_default_account(user_id: uuid.UUID, username: str, session: AsyncSession):
    """Create a default account for a new user"""
    # Create the account
    account = Account(
        name=f"{username} - account",
        is_active=True
    )
    session.add(account)
    await session.flush()  # Get the account ID
    
    # Link user to account
    user_account = UserAccount(
        user_id=user_id,
        account_id=account.id,
        is_active=True
    )
    session.add(user_account)
    await session.commit()
    
    return account