from fastapi import APIRouter, Depends
from ..Infrastructure.users import current_active_user, User
from ..Infrastructure.db import get_async_session
from ..Services.accounts_service.accounts_service import get_user_accounts
from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_accounts_endpoint(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    accounts = await get_user_accounts(session, user)
    return accounts
