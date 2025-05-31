from fastapi import APIRouter, Depends
from ..users import current_active_user


router = APIRouter(
    prefix="/transfer",
    tags=["balance"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get():
    return {"transfer": 1}
