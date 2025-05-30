import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from .accounts import Account, UserAccount

async def create_default_account(user_id: uuid.UUID, username: str, session: AsyncSession):
    """Create a default account for a new user"""
    # Create the account
    account = Account(
        name=f"{username} - account",
        isActive=True
    )
    session.add(account)
    await session.flush()  # Get the account ID
    
    # Link user to account
    user_account = UserAccount(
        userId=user_id,
        accountId=account.id,
        isActive=True
    )
    session.add(user_account)
    await session.commit()
    
    return account