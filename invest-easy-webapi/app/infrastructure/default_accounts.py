from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.accounts import Account, UserAccount
from ..domain.balance import Balance


async def create_default_account(
    user_id: uuid.UUID, username: str, session: AsyncSession
):
    """Create default accounts for a new user"""
    # Create the account
    account_ov = Account(
        name=f"{username} - overview account",
        ccy="HKD",
        is_virtual=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    account_hkd = Account(
        name=f"{username} - HKD account",
        ccy="HKD",
        is_virtual=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    account_usd = Account(
        name=f"{username} - USD account",
        ccy="USD",
        is_virtual=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    account_cnh = Account(
        name=f"{username} - CNH account",
        ccy="CNH",
        is_virtual=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(account_ov)
    session.add(account_hkd)
    session.add(account_usd)
    session.add(account_cnh)
    await session.flush()  # Get the account ID

    # Link user to account
    user_account_ov = UserAccount(user_id=user_id, account_id=account_ov.id)
    user_account_hkd = UserAccount(user_id=user_id, account_id=account_hkd.id)
    user_account_usd = UserAccount(user_id=user_id, account_id=account_usd.id)
    user_account_cnh = UserAccount(user_id=user_id, account_id=account_cnh.id)
    session.add(user_account_ov)
    session.add(user_account_hkd)
    session.add(user_account_usd)
    session.add(user_account_cnh)
    await session.flush()

    balance_ov = Balance(
        user_account_id=user_account_ov.id,
        balance=0.0,
        ccy="HKD",
        is_virtual=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    balance_hkd = Balance(
        user_account_id=user_account_hkd.id,
        balance=0.0,
        ccy="HKD",
        is_virtual=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    balance_usd = Balance(
        user_account_id=user_account_usd.id,
        balance=0.0,
        ccy="USD",
        is_virtual=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    balance_cnh = Balance(
        user_account_id=user_account_cnh.id,
        balance=0.0,
        ccy="CNH",
        is_virtual=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    session.add(balance_ov)
    session.add(balance_hkd)
    session.add(balance_usd)
    session.add(balance_cnh)
    await session.commit()

    return True
