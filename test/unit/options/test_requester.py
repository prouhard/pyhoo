import json
from unittest.mock import AsyncMock, patch

import pytest

from pynance.models.options import OptionsData
from pynance.options.getter import GetTickerOptionsTask
from pynance.options.requester import OptionsRequester

with open("test/unit/responses/options.json", "r") as file:
    mock_options = json.load(file)


@pytest.mark.asyncio
@patch.object(GetTickerOptionsTask, "run")
async def test_requester_request(mock_getter_run: AsyncMock) -> None:
    tickers = ["NVDA"]
    max_concurrent_calls = 1

    mock_getter_run.return_value = [OptionsData(**response) for response in mock_options["optionChain"]["result"]]

    requester = OptionsRequester(
        tickers=tickers,
        max_concurrent_calls=max_concurrent_calls,
    )

    options = await requester.request()

    assert options.columns.tolist() == [
        "underlyingSymbol",
        "type",
        "contractSymbol",
        "strike",
        "currency",
        "lastPrice",
        "change",
        "percentChange",
        "ask",
        "contractSize",
        "expiration",
        "lastTradeDate",
        "impliedVolatility",
        "inTheMoney",
        "volume",
        "bid",
        "openInterest",
    ]

    assert len(options) == 3
