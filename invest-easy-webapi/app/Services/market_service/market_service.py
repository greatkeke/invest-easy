from typing import Annotated, List
from fastapi import Depends
from pandas import DataFrame
from ...infrastructure.futu_api_service import FutuApiService


class MarketService:
    def __init__(
        self, futu_api_svc: Annotated[FutuApiService, Depends(FutuApiService)]
    ):
        self.futu_api_svc = futu_api_svc

    def get_market_snapshot(self, code_list: List[str]):
        data = self.futu_api_svc.get_market_snapshot(code_list=code_list)
        return data

    def get_rt_data(self, code: str):
        """
        Get real-time tick data for a stock

        Args:
            code: Stock code (e.g. 'HK.00700')

        Returns:
            List of dicts containing real-time tick data
        """
        data = self.futu_api_svc.get_rt_data(code=code)
        return data
