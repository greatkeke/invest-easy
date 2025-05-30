from typing import Optional
from uuid import UUID
from fastapi import Request, Depends
from fastapi_users import FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.manager import BaseUserManager
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from .db import AccessToken, User, get_access_token_db, get_async_session, get_user_db
from .accounts.defaultAccounts import create_default_account


# User manager
class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        async for session in get_async_session():
            await create_default_account(
                user_id=user.id, username=str(user.username), session=session
            )
            break


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[User, UUID] = Depends(get_user_db),
):
    yield UserManager(user_db)


SECRET = "SECRET"

# Authentication setup
transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=transport,
    get_strategy=get_database_strategy,
)

# FastAPI Users setup
fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
