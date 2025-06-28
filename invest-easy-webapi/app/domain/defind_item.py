from enum import Enum
from sqlalchemy import UUID, Integer, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import mapped_column
from .base_domain import Base


class DefinedAttributeType(Enum):
    TEXT = 0
    NUMBER = 1
    BOOLEAN = 2
    EMAIL = 3
    PHONE = 4
    ADDRESS = 5
    OPTIONS = 6


class DefinedGroup(Base):
    __tablename__ = "defined_group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)


class DefinedItem(Base):
    __tablename__ = "defined_items"

    id = mapped_column(Integer, primary_key=True)
    group_id = mapped_column(Integer, nullable=False)
    name = mapped_column(String, nullable=False)
    value = mapped_column(String, nullable=False)
    type = mapped_column(SQLEnum(DefinedAttributeType), nullable=False)
    editable = mapped_column(Boolean, default=True)
    secret = mapped_column(Boolean, default=False)


class DefinedValue(Base):
    __tablename__ = "defined_value"

    id = mapped_column(Integer, primary_key=True)
    item_id = mapped_column(Integer, nullable=False)
    user_id = mapped_column(UUID, nullable=True)
    value = mapped_column(String, nullable=False)
