from typing import Any, Dict, List

import aiohttp

from pynance.config import logging
from pynance.models.options import OptionsData


class GetTickerOptionsTask:

    _ticker: str

    _BASE_URL = "https://query2.finance.yahoo.com"

    def __init__(
        self,
        ticker: str,
    ) -> None:
        self._ticker = ticker

    async def run(self, session: aiohttp.ClientSession) -> List[OptionsData]:
        logging.info(f"Getting URL {self._url} ...")
        response = await session.request("GET", url=self._url)
        data = await response.json()
        logging.info(f"Received data for {self._url} !")
        return self._parse_data(data)

    @property
    def _url(self):
        return f"{self._BASE_URL}/v7/finance/options/{self._ticker}"

    @staticmethod
    def _parse_data(data: Dict[str, Any]) -> List[OptionsData]:
        return [OptionsData(**response) for response in data["optionChain"]["result"]]
