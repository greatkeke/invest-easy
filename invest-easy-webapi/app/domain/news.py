from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from .base_domain import Base


class NewsItem(Base):
    __tablename__ = "news"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    content = Column(String, nullable=True)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, server_default=func.now())
    source = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    url = Column(String, nullable=True)
    
