from typing import Any, Dict, List

import aiohttp

from pynance.config import logging
from pynance.models.stock import Interval, StockData


class GetTickerStockTask:

    _ticker: str
    _start_timestamp: int
    _end_timestamp: int
    _interval: Interval

    _BASE_URL = "https://query1.finance.yahoo.com"

    def __init__(
        self,
        ticker: str,
        start_timestamp: int,
        end_timestamp: int,
        interval: Interval,
    ) -> None:
        self._ticker = ticker
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._interval = interval

    async def run(self, session: aiohttp.ClientSession) -> List[StockData]:
        logging.info(f"Getting URL {self._url} ...")
        response = await session.request("GET", url=self._url)
        data = await response.json()
        logging.info(f"Received data for {self._url} !")
        return self._parse_data(data)

    @property
    def _url(self):
        return (
            f"{self._BASE_URL}/v8/finance/chart/{self._ticker}?"
            f"period1={self._start_timestamp}&"
            f"period2={self._end_timestamp}&"
            f"interval={self._interval.value}"
        )

    @staticmethod
    def _parse_data(data: Dict[str, Any]) -> List[StockData]:
        return [StockData(**response) for response in data["chart"]["result"]]
