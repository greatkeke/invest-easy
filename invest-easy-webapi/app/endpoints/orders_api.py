from typing import List, Optional
from fastapi import APIRouter, Depends
from ..infrastructure.users import current_active_user, User
from ..services.orders_service import OrdersService


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_orders_endpoint(
    user: User = Depends(current_active_user),
    orders_service: OrdersService = Depends(OrdersService),
    page: Optional[int] = 1,
    page_size: Optional[int] = 5
):
    # Convert optional parameters to concrete values
    page_num = page if page is not None else 1
    size = page_size if page_size is not None else 5
    
    orders = await orders_service.get_user_orders(user.id, page=page_num, page_size=size)
    return orders  # Service now returns properly formatted paginated response
