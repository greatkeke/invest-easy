from datetime import datetime
import uuid
from sqlalchemy import UUID, Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column
from .base_domain import Base


class NewsItem(Base):
    __tablename__ = "news"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    content = Column(String, nullable=True)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, default=datetime.now(), index=True)
    source = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    url = Column(String, nullable=False, index=True)
    # override created_at with index
    created_at = Column(DateTime, default=datetime.now(), nullable=False, index=True)

