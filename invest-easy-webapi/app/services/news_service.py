from typing import List
from fastapi import Depends
from ..infrastructure.users import User
from ..domain.news import NewsItem
from newsapi import NewsApiClient
from typing import List
from datetime import datetime
import logging
from fastapi import HTTPException
from ..domain.news import NewsItem
from ..domain.users import User
from ..config import settings

logger = logging.getLogger(__name__)


class NewsService:
    async def get_paginated_news(
        self, user: User, page: int, page_size: int
    ) -> List[NewsItem]:
        """
        Get paginated news items for the given user.

        Args:
            user: The user requesting news
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
            logger.info(
                f"Fetching news for user {user.id}, page {page}, size {page_size}"
            )
            newsapi = NewsApiClient(api_key=settings.news_api_key)
            response = newsapi.get_top_headlines(category="business", page=page, page_size=page_size)
            if(response["status"] == "ok"):
                return [
                    NewsItem(
                        title=article["title"],
                        author=article["author"],
                        description = article["description"],
                        url= article["url"],
                        image_url = article["urlToImage"],
                        published_at = article["publishedAt"],
                        source = article["source"]["name"],
                        content = article["content"]
                    ) for article in response["articles"]
                ]
            return []


        except Exception as e:
            logger.error(f"Failed to fetch news: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch news items")
