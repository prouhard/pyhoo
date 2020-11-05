import json
from unittest.mock import AsyncMock, patch

import pytest

from pyhoo.getter import GetTickerDataTask
from pyhoo.models.chart import Interval
from pyhoo.requester import Requester

with open("tests/unit/responses/chart.json", "r") as file:
    mock_chart = json.load(file)

with open("tests/unit/responses/fundamentals.json", "r") as file:
    mock_fundamentals = json.load(file)

with open("tests/unit/responses/options.json", "r") as file:
    mock_options = json.load(file)


@pytest.mark.asyncio
@patch.object(GetTickerDataTask, "run")
async def test_requester_request_chart(mock_getter_run: AsyncMock) -> None:
    tickers = ["NVDA"]
    period1 = 1594647000
    period2 = 1594992600
    interval = Interval.ONE_DAY.value
    path = "v8/finance/chart"
    max_concurrent_calls = 1

    mock_getter_run.return_value = mock_chart

    requester = Requester(
        path=path,
        tickers=tickers,
        period1=period1,
        period2=period2,
        interval=interval,
        max_concurrent_calls=max_concurrent_calls,
    )

    chart = await requester.request()

    assert chart == [mock_chart]


@pytest.mark.asyncio
@patch.object(GetTickerDataTask, "run")
async def test_requester_request_fundamentals(mock_getter_run: AsyncMock) -> None:
    tickers = ["NVDA"]
    period1 = 1485820800
    period2 = 1517356800
    type = "annualWorkInProcess,annualConstructionInProgress"
    path = "ws/fundamentals-timeseries/v1/finance/timeseries"
    max_concurrent_calls = 1

    mock_getter_run.return_value = mock_fundamentals

    requester = Requester(
        path=path,
        tickers=tickers,
        period1=period1,
        period2=period2,
        type=type,
        max_concurrent_calls=max_concurrent_calls,
    )

    fundamentals = await requester.request()

    assert fundamentals == [mock_fundamentals]


@pytest.mark.asyncio
@patch.object(GetTickerDataTask, "run")
async def test_requester_request_options(mock_getter_run: AsyncMock) -> None:
    tickers = ["NVDA"]
    path = "v7/finance/options"
    max_concurrent_calls = 1

    mock_getter_run.return_value = mock_options

    requester = Requester(
        path=path,
        tickers=tickers,
        max_concurrent_calls=max_concurrent_calls,
    )

    options = await requester.request()

    assert options == [mock_options]
