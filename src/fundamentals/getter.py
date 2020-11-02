import json
from functools import reduce
from typing import Any, Dict

import aiohttp

from config import FUNDAMENTALS_CONFIG_FILE, logging
from models.fundamentals import Frequency, FundamentalsData

with open(FUNDAMENTALS_CONFIG_FILE, 'r') as config_file:
    FUNDAMENTALS_CONFIG = json.load(config_file)


class GetTickerFundamentalsTask:

    _ticker: str
    _start_timestamp: int
    _end_timestamp: int
    _frequency: Frequency

    _BASE_URL = 'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries'

    def __init__(self, ticker: str, start_timestamp: int, end_timestamp: int, frequency: Frequency) -> None:
        self._ticker = ticker
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._frequency = frequency

    async def run(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        logging.info(f'Getting URL {self._url} ...')
        response = await session.request('GET', url=self._url)
        data = await response.json()
        logging.info(f'Received data for {self._url} !')
        return self._parse_data(data)

    @property
    def _url(self) -> str:
        return (
            f'{self._BASE_URL}/{self._ticker}?'
            f'period1={self._start_timestamp}&'
            f'period2={self._end_timestamp}&'
            f'type={self._types}'
        )

    @property
    def _types(self) -> str:
        return ','.join(
            f'{self._frequency.value}{_type}'
            for _type in reduce(lambda x, y: x + y, FUNDAMENTALS_CONFIG.values())
        )

    @staticmethod
    def _parse_data(data: Dict[str, Any]) -> FundamentalsData:
        return [FundamentalsData(**response) for response in data['timeseries']['result']]
