from typing import Annotated, List
from fastapi import Depends
from pandas import DataFrame
from ...Infrastructure.futu_api_service import futu_api_service


class market_service:
    def __init__(
        self, futu_api_svc: Annotated[futu_api_service, Depends(futu_api_service)]
    ):
        self.futu_api_svc = futu_api_svc

    def get_market_snapshot(self, code_list: List[str]):
        data = self.futu_api_svc.get_market_snapshot(code_list=code_list)
        return data
