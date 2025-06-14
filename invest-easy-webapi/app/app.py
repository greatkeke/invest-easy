from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .domain.users import User
from .domain.instruments import Instrument
from .domain.positions import Position
from .infrastructure.db import create_tables, get_async_session
from .infrastructure.users import fastapi_users, auth_backend, current_active_user
from .infrastructure.schemas import UserRead, UserCreate, UserUpdate
from .infrastructure.futu_api_service import FutuApiService
from .endpoints import balance_api, accounts_api, market_api, trade_api, position_api, orders_api, watch_list_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_tables()
    
    # Initialize market instruments
    async for session in get_async_session():
        try:
            futu_service = FutuApiService(session=session)
            await futu_service.initialize_all_markets_instruments()
        finally:
            await session.close()
    
    yield


app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/users",
    tags=["users"],
)

app.include_router(accounts_api.router, prefix="/api")
app.include_router(balance_api.router, prefix="/api")
app.include_router(market_api.router, prefix="/api")
app.include_router(trade_api.router, prefix="/api")
app.include_router(position_api.router, prefix="/api")
app.include_router(orders_api.router, prefix="/api")
app.include_router(watch_list_api.router, prefix="/api")


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


@app.get("/api/authenticated-user/name")
async def authenticated_route(user: Annotated[User, Depends(current_active_user)]):
    return {"username": user.username}
