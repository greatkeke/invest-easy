from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from .users import fastapi_users, auth_backend, current_active_user
from .users import User
from .schemas import UserRead, UserCreate, UserUpdate
from .db import create_tables, get_async_session
from .accounts.accounts import get_user_accounts
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import transfer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(transfer.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins_list,  # Uses parsed origins from env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authenticated-user/name")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"username": user.username}


@app.get("/accounts")
async def get_user_accounts_endpoint(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    accounts = await get_user_accounts(session, user)
    return accounts
