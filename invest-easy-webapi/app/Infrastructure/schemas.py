from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate

# Pydantic schemas
class UserRead(BaseUser):
    username: str


class UserCreate(BaseUserCreate):
    username: str


class UserUpdate(BaseUserUpdate):
    username: str
