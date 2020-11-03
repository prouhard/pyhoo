import asyncio
from typing import Iterable

import aiohttp
import pandas as pd

from pynance.options.getter import GetTickerOptionsTask


class OptionsRequester:

    _tickers: Iterable[str]
    _max_concurrent_calls: int

    def __init__(
        self,
        tickers: Iterable[str],
        max_concurrent_calls: int = 100,
    ) -> None:
        self._tickers = tickers
        self._max_concurrent_calls = max_concurrent_calls

    async def request(self) -> pd.DataFrame:
        """Asynchronously fire requests by ticker thanks to the `GetTickerOptionsTask`."""
        connector = aiohttp.TCPConnector(limit=self._max_concurrent_calls)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for ticker in self._tickers:
                tasks.append(GetTickerOptionsTask(ticker=ticker).run(session=session))
            batch_ticker_options_data = await asyncio.gather(*tasks, return_exceptions=True)
            return pd.DataFrame(
                [
                    record
                    for ticker_options_data in batch_ticker_options_data
                    for ticker_option_data in ticker_options_data
                    for record in ticker_option_data.to_records()
                ],
            )
