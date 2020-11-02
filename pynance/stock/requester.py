import asyncio
from typing import Iterable

import aiohttp
import pandas as pd

from pynance.models.stock import Interval
from pynance.stock.getter import GetTickerStockTask


class StockRequester:

    _tickers: Iterable[str]
    _start_timestamp: int
    _end_timestamp: int
    _interval: Interval
    _max_concurrent_calls: int

    def __init__(
        self,
        tickers: Iterable[str],
        start_timestamp: int,
        end_timestamp: int,
        interval: Interval = Interval.ONE_DAY,
        max_concurrent_calls: int = 100,
    ) -> None:
        self._tickers = tickers
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._interval = interval
        self._max_concurrent_calls = max_concurrent_calls

    async def request(self) -> pd.DataFrame:
        """Asynchronously fire requests by ticker thanks to the `GetTickerStockTask`."""
        connector = aiohttp.TCPConnector(limit=self._max_concurrent_calls)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for ticker in self._tickers:
                tasks.append(
                    GetTickerStockTask(
                        ticker=ticker,
                        start_timestamp=self._start_timestamp,
                        end_timestamp=self._end_timestamp,
                        interval=self._interval,
                    ).run(session=session),
                )
            batch_ticker_stocks_data = await asyncio.gather(*tasks, return_exceptions=True)
            return pd.DataFrame(
                [
                    record
                    for ticker_stocks_data in batch_ticker_stocks_data
                    for ticker_stock_data in ticker_stocks_data
                    for record in ticker_stock_data.to_records()
                ],
            )
