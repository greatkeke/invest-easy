from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from .users import fastapi_users, auth_backend, User, current_active_user
from .schemas import UserRead, UserCreate, UserUpdate
from .db import create_tables
from fastapi.middleware.cors import CORSMiddleware
from .config import settings



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


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
