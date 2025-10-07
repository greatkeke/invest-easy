import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import RotatingFileHandler
from .config import settings
from .domain.users import User
from .domain.instruments import Instrument
from .domain.positions import Position
from .infrastructure.db import create_tables, get_async_session
from .infrastructure.users import fastapi_users, auth_backend, current_active_user
from .infrastructure.schemas import UserRead, UserCreate, UserUpdate
from .infrastructure.futu_api_service import FutuApiService
from .infrastructure.akshare_service import AkshareService
from .endpoints import (
    balance_api,
    accounts_api,
    market_api,
    trade_api,
    position_api,
    orders_api,
    watch_list_api,
    settings_api,
    news_api,
    exchange_api,
    report_api
)
from .infrastructure.default_settings import predefined_settings


# Configure logging
log_path = settings.log_path
os.makedirs(log_path, exist_ok=True)

# Convert log level from string to logging constant
log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

# Create rotating file handler (50MB max size)
max_bytes = settings.log_max_size * 1024 * 1024  # Convert MB to bytes
file_handler = RotatingFileHandler(
    os.path.join(log_path, "app.log"),
    maxBytes=max_bytes,
    backupCount=settings.log_backup_count
)
file_handler.setLevel(log_level)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Get root logger and add handlers
root_logger = logging.getLogger()
root_logger.setLevel(log_level)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Configure specific loggers
logging.getLogger("uvicorn").setLevel(log_level)
logging.getLogger("uvicorn.error").addHandler(file_handler)
logging.getLogger("uvicorn.access").addHandler(file_handler)
logging.getLogger("sqlalchemy").addHandler(file_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_tables()

    # Initialize market instruments
    async for session in get_async_session():
        try:
            futu_service = FutuApiService(session=session)
            akshare_service = AkshareService(session=session)
            await futu_service.initialize_all_markets_instruments()
            if settings.enable_ak_initialization:
                await akshare_service.initialize_snapshots_table()
            await predefined_settings(session)
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
app.include_router(settings_api.router, prefix="/api")
app.include_router(news_api.router, prefix="/api")
app.include_router(exchange_api.router, prefix="/api")
app.include_router(report_api.router, prefix="/api")


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
