from fastapi import APIRouter, Depends
from ..infrastructure.users import current_active_user, User
from ..services.accounts_service import AccountService


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_accounts_endpoint(
    user: User = Depends(current_active_user),
    accountSvc: AccountService = Depends(AccountService),
):
    accounts = await accountSvc.get_user_accounts(user)
    return accounts


@router.get("/balances")
async def get_user_accounts_balances(
    user: User = Depends(current_active_user),
    accountSvc: AccountService = Depends(AccountService),
    is_overview: bool = False,
):
    accounts = await accountSvc.get_user_accounts_balances(user, is_overview)
    return accounts
