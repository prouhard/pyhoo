from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, DefaultDict, Deque


class MockResponse:
    def __init__(self, json: Any) -> None:
        self._json = json

    async def json(self) -> Any:
        return self._json


class MockSession:
    """Mock aiohttp session providing custom mock responses by URI and resource verb."""

    _responses: DefaultDict[str, DefaultDict[str, Deque[MockResponse]]]

    def __init__(self) -> None:
        """Set the responses mapping to an empty dict."""
        self._responses = defaultdict(lambda: defaultdict(deque))

    def add(self, url: str, method: str, response: Any) -> None:
        """Add a mock response to a specific URI and resource verb. Responses are queued."""
        self._responses[url][method].append(MockResponse(response))

    async def request(self, method: str, url: str) -> MockResponse:
        """Pop the first response stored for the specified URI and resource verb."""
        return self._responses[url][method].popleft()

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def __aenter__(self) -> MockSession:
        return self
