from fastapi import APIRouter, Depends
from ..infrastructure.users import current_active_user, User
from ..services.news_service import NewsService


router = APIRouter(
    prefix="/news",
    tags=["news"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_news_endpoint(
    user: User = Depends(current_active_user),
    newsSvc: NewsService = Depends(NewsService),
    page: int = 1,
    page_size: int = 10
):
    news = await newsSvc.get_paginated_news(user, page, page_size)
    return news
