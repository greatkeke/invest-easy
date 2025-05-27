from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate

# Pydantic schemas
class UserRead(BaseUser):
    pass


class UserCreate(BaseUserCreate):
    pass


class UserUpdate(BaseUserUpdate):
    pass
