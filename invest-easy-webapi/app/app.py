from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from .Infrastructure.users import User, fastapi_users, auth_backend, current_active_user
from .Infrastructure.schemas import UserRead, UserCreate, UserUpdate
from .Infrastructure.db import create_tables
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .Endpoints import balance_api, accounts_api, market_api, trade_api


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

app.include_router(accounts_api.router)
app.include_router(balance_api.router)
app.include_router(market_api.router)
app.include_router(trade_api.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins_list,  # Uses parsed origins from env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"health": "ok"}


@app.get("/authenticated-user/name")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"username": user.username}
