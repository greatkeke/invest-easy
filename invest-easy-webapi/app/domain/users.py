# Database setup
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from .base_domain import Base


# User model
class User(SQLAlchemyBaseUserTableUUID, Base):
    username = mapped_column(String(30), nullable=False)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass
