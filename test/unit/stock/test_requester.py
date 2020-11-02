import json
from unittest.mock import AsyncMock, patch

import pytest

from pynance.models.stock import Interval, StockData
from pynance.stock.getter import GetTickerStockTask
from pynance.stock.requester import StockRequester

with open("test/unit/responses/stock.json", "r") as file:
    mock_stock = json.load(file)


@pytest.mark.asyncio
@patch.object(GetTickerStockTask, "run")
async def test_requester_request(mock_getter_run: AsyncMock) -> None:
    tickers = ["NVDA"]
    start_timestamp = 1594647000
    end_timestamp = 1594992600
    interval = Interval.ONE_DAY
    max_concurrent_calls = 1

    mock_getter_run.return_value = [StockData(**response) for response in mock_stock["chart"]["result"]]

    requester = StockRequester(
        tickers=tickers,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        interval=interval,
        max_concurrent_calls=max_concurrent_calls,
    )

    stock = await requester.request()

    assert stock.columns.tolist() == [
        "timestamp",
        "high",
        "low",
        "volume",
        "open",
        "close",
        "adjclose",
        "currency",
        "symbol",
        "exchangeName",
        "instrumentType",
        "firstTradeDate",
        "regularMarketTime",
        "gmtoffset",
        "timezone",
        "exchangeTimezoneName",
        "regularMarketPrice",
        "chartPreviousClose",
        "priceHint",
        "dataGranularity",
        "range",
    ]

    assert len(stock) == 5
