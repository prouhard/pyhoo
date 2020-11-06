from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, DefaultDict, Deque, Dict, Tuple


class MockResponse:
    def __init__(self, json: Any) -> None:
        self._json = json

    async def json(self) -> Any:
        return self._json


class MockSession:
    """Mock aiohttp session providing custom mock responses by URI and resource verb."""

    _responses: DefaultDict[str, DefaultDict[str, DefaultDict[Tuple[Any, ...], Deque[MockResponse]]]]

    def __init__(self) -> None:
        """Set the responses mapping to an empty dict."""
        self._responses = defaultdict(lambda: defaultdict(lambda: defaultdict(deque)))

    def add(self, url: str, params: Dict[str, Any], method: str, response: Any) -> None:
        """Add a mock response to a specific URI and resource verb. Responses are queued."""
        hashable_params = self._hashify_params(params)
        self._responses[url][method][hashable_params].append(MockResponse(response))

    async def request(self, method: str, url: str) -> MockResponse:
        """Pop the first response stored for the specified URI and resource verb."""
        params = self._hashify_params(self._parse_params(url))
        url_without_params, *_ = url.split("?")
        return self._responses[url_without_params][method][params].popleft()

    def _parse_params(self, url: str) -> Dict[str, Any]:
        _, *query = url.split("?")
        if query:
            return {param.split("=")[0]: param.split("=")[1] for param in query[0].split("&")}
        return {}

    @staticmethod
    def _hashify_params(params: Dict[str, Any]) -> Tuple[Tuple[str, str], ...]:
        return tuple(sorted([(key, str(value)) for key, value in params.items()]))

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def __aenter__(self) -> MockSession:
        return self
