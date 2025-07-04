from enum import Enum
from typing import Optional
from sqlalchemy import UUID, Integer, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import mapped_column
from .base_domain import Base


class DefinedItemType(Enum):
    Empty = 0
    TEXT = 1
    NUMBER = 2
    BOOLEAN = 3
    EMAIL = 4
    PHONE = 5
    ADDRESS = 6
    OPTIONS = 7
    SINGLE = 8


class DefinedGroup(Base):
    __tablename__ = "defined_group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)


from typing import Optional
from sqlalchemy.orm import Mapped


class DefinedItem(Base):
    """Represents a defined configuration item with type safety and validation."""

    __tablename__ = "defined_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    note: Mapped[Optional[str]] = mapped_column(String)
    value: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[DefinedItemType] = mapped_column(
        SQLEnum(DefinedItemType), nullable=False
    )
    editable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    secret: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __init__(
        self,
        name: str,
        value: str,
        type: DefinedItemType,
        editable: bool = True,
        secret: bool = False,
        note: Optional[str] = None,
    ):
        self.name = name
        self.value = value
        self.type = type
        self.editable = editable
        self.secret = secret
        self.note = note


class DefinedValue(Base):
    __tablename__ = "defined_value"

    id = mapped_column(Integer, primary_key=True)
    item_id = mapped_column(Integer, nullable=False)
    user_id = mapped_column(UUID, nullable=True)
    value = mapped_column(String, nullable=False)
