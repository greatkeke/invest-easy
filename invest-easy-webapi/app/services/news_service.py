from typing import Annotated, List
from fastapi import Depends
from ..domain.news import NewsItem
from newsapi import NewsApiClient
from typing import List
from datetime import datetime
import logging
from fastapi import HTTPException
from ..domain.news import NewsItem
from ..config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..infrastructure.db import get_async_session
from dateutil import parser
from asyncer import asyncify

logger = logging.getLogger(__name__)


class NewsService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
        self.session = session
        self.newsapi = NewsApiClient(api_key=settings.news_api_key)

    async def get_paginated_news(self, page: int, page_size: int) -> List[NewsItem]:
        """
        Get paginated news items for the given user.

        Args:
            page: Page number (1-based)
            page_size: Number of items per page

        Returns:
            List of NewsItem objects

        Raises:
            HTTPException: If invalid pagination parameters are provided
        """
        # Validate pagination parameters
        if page < 1 or page_size < 1 or page_size > 100:
            logger.warning(
                f"Invalid pagination params - page: {page}, page_size: {page_size}"
            )
            raise HTTPException(
                status_code=400,
                detail="Invalid pagination parameters. Page must be >= 1 and page_size between 1-100",
            )

        try:
            # Check for latest news in DB
            latest_news = await self.session.execute(
                select(NewsItem)
                .order_by(NewsItem.created_at.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            latest_news = latest_news.scalars().first()

            # If no news or older than 1 hour, fetch from NewsAPI
            if (
                not latest_news
                or (datetime.now() - latest_news.created_at).total_seconds() > 3600
            ):
                response = await asyncify(self.newsapi.get_top_headlines)(
                    category="business", page=page, page_size=page_size
                )


                if response["status"] == "ok":
                    # Convert and store new articles
                    # Create news items and filter out existing ones
                    news_items_to_insert = []
                    news_items_to_return = []
                    for article in response["articles"]:
                        news_item = NewsItem(
                            title=article["title"],
                            author=article["author"],
                            description=article["description"],
                            url=article["url"],
                            image_url=article["urlToImage"],
                            published_at=parser.parse(article["publishedAt"]),
                            source=article["source"]["name"],
                            content=article["content"],
                            created_at=datetime.now(),
                        )
                        news_items_to_return.append(news_item)
                        # Check if news item with this URL already exists
                        existing = await self.session.execute(
                            select(NewsItem).where(NewsItem.url == news_item.url)
                        )
                        if not existing.scalars().first():
                            news_items_to_insert.append(news_item)

                    if news_items_to_insert:
                        self.session.add_all(news_items_to_insert)
                        await self.session.commit()
                    return news_items_to_return
                return []

            # Return paginated results from DB
            db_news = await self.session.execute(
                select(NewsItem)
                .order_by(NewsItem.published_at.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            return list(db_news.scalars().all())

        except Exception as e:
            logger.error(f"Failed to fetch news: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch news items")
