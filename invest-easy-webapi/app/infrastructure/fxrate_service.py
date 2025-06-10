from datetime import datetime


class FxRateService:
    def __init__(self):
        pass

    def get_fxrate_by_ccy(self, ccy: str, date: datetime = datetime.now()):
        if ccy == "HKD":
            return 1
        if ccy == "USD":
            return 780 / 100
        if ccy == "CNH":
            return 109 / 100
        return 1
