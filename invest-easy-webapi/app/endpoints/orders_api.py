from typing import List
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
):
    orders = await orders_service.get_user_orders(user.id)
    return orders
