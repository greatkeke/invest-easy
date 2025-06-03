from sqlalchemy.ext.asyncio import AsyncSession
from ...Domain.users import User
from ...Domain.accounts import Account, UserAccount
from sqlalchemy import select


async def get_user_accounts(session: AsyncSession, user: User):
    result = await session.execute(
        select(Account.id, Account.name)
        .join(
            UserAccount,
            UserAccount.account_id == Account.id and UserAccount.is_active == True,
        )
        .where(UserAccount.user_id == user.id and Account.is_active == True)
    )
    return [{"id": str(row[0]), "name": row[1]} for row in result.all()]
