from typing import Any, Dict, cast

import aiohttp

from pyhoo.types import ApiResponse


class GetTickerDataTask:

    _path: str
    _ticker: str
    _params: Dict[str, Any]

    _BASE_URL = "https://query2.finance.yahoo.com"

    def __init__(
        self,
        path: str,
        ticker: str,
        **params: Any,
    ) -> None:
        self._path = path
        self._ticker = ticker
        self._params = params

    async def run(self, session: aiohttp.ClientSession) -> Dict[str, ApiResponse]:
        response = await session.request("GET", url=self._url)
        data = cast(Dict[str, ApiResponse], await response.json())
        return data

    @property
    def _url(self) -> str:
        url = f"{self._BASE_URL}/{self._path}/{self._ticker}"
        if self._params:
            url = f"{url}?{self._format_params()}"
        return url

    def _format_params(self) -> str:
        return "&".join(f"{name}={value}" for name, value in self._params.items())
