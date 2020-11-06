import asyncio
from typing import Any, Dict, Iterable, List, cast

import aiohttp

from pyhoo.getter import GetTickerDataTask
from pyhoo.types import ApiResponse


class Requester:

    _path: str
    _tickers: Iterable[str]
    _max_concurrent_calls: int
    _params: Dict[str, Any]

    def __init__(
        self,
        path: str,
        tickers: Iterable[str],
        max_concurrent_calls: int = 100,
        **params: Any,
    ) -> None:
        self._path = path
        self._tickers = tickers
        self._params = params
        self._max_concurrent_calls = max_concurrent_calls

    async def request(self) -> List[Dict[str, ApiResponse]]:
        """Asynchronously fire requests by ticker thanks to the `GetTickerDataTask`."""
        connector = aiohttp.TCPConnector(limit=self._max_concurrent_calls)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for ticker in self._tickers:
                tasks.append(
                    GetTickerDataTask(
                        path=self._path,
                        ticker=ticker,
                        **self._params,
                    ).run(session=session)
                )
            responses = cast(
                List[Dict[str, ApiResponse]],
                await asyncio.gather(*tasks, return_exceptions=False),
            )
            return responses
