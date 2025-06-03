# Database setup
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
)
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
)


class Base(DeclarativeBase):
    pass


# User model
class User(SQLAlchemyBaseUserTableUUID, Base):
    username = mapped_column(String(30), unique=True, nullable=False)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass

