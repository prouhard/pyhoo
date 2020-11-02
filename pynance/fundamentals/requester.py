import asyncio
from typing import Iterable

import aiohttp
import pandas as pd

from pynance.fundamentals.getter import GetTickerFundamentalsTask
from pynance.models.fundamentals import Frequency


class TickerFundamentalsRequester:

    _tickers: Iterable[str]
    _start_timestamp: int
    _end_timestamp: int
    _frequency: Frequency
    _max_concurrent_calls: int

    def __init__(
        self,
        tickers: Iterable[str],
        start_timestamp: int,
        end_timestamp: int,
        frequency: Frequency = Frequency.ANNUAL,
        max_concurrent_calls: int = 100,
    ) -> None:
        self._tickers = tickers
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._frequency = frequency
        self._max_concurrent_calls = max_concurrent_calls

    async def request(self) -> pd.DataFrame:
        """Asynchronously fire requests by ticker thanks to the `GetTickerFundamentalsTask`."""
        connector = aiohttp.TCPConnector(limit=self._max_concurrent_calls)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for ticker in self._tickers:
                tasks.append(
                    GetTickerFundamentalsTask(
                        ticker=ticker,
                        start_timestamp=self._start_timestamp,
                        end_timestamp=self._end_timestamp,
                        frequency=self._frequency,
                    ).run(session=session),
                )
            batch_ticker_fundamentals_data = await asyncio.gather(
                *tasks, return_exceptions=True
            )
            return pd.DataFrame(
                [
                    record
                    for ticker_fundamentals_data in batch_ticker_fundamentals_data
                    for ticker_fundamental_data in ticker_fundamentals_data
                    for record in ticker_fundamental_data.to_records()
                ],
            )
