import json
from typing import cast

import pytest
from aiohttp import ClientSession

from pyhoo.getter import GetTickerDataTask
from pyhoo.models.chart import Interval

with open("tests/unit/responses/chart.json", "r") as file:
    mock_chart = json.load(file)

with open("tests/unit/responses/fundamentals.json", "r") as file:
    mock_fundamentals = json.load(file)

with open("tests/unit/responses/options.json", "r") as file:
    mock_options = json.load(file)


from tests.mock.session import MockSession


@pytest.mark.asyncio
async def test_getter_run_chart() -> None:
    ticker = "NVDA"
    period1 = 1594647000
    period2 = 1594992600
    interval = Interval.ONE_DAY.value
    path = "v8/finance/chart"
    session = MockSession()
    url = (
        f"{GetTickerDataTask._BASE_URL}/{path}/{ticker}?"
        f"period1={period1}&"
        f"period2={period2}&"
        f"interval={interval}"
    )

    session.add(url, "GET", mock_chart)

    task = GetTickerDataTask(
        path=path,
        ticker=ticker,
        period1=period1,
        period2=period2,
        interval=interval,
    ).run(session=cast(ClientSession, session))

    chart = await task

    assert chart == mock_chart


@pytest.mark.asyncio
async def test_getter_run_fundamentals() -> None:
    ticker = "NVDA"
    period1 = 1485820800
    period2 = 1517356800
    type = "annualWorkInProcess,annualConstructionInProgress"
    path = "ws/fundamentals-timeseries/v1/finance/timeseries"
    session = MockSession()
    url = f"{GetTickerDataTask._BASE_URL}/{path}/{ticker}?period1={period1}&period2={period2}&type={type}"

    session.add(url, "GET", mock_fundamentals)

    task = GetTickerDataTask(
        path=path,
        ticker=ticker,
        period1=period1,
        period2=period2,
        type=type,
    ).run(session=cast(ClientSession, session))

    fundamentals = await task

    assert fundamentals == mock_fundamentals


@pytest.mark.asyncio
async def test_getter_run_options() -> None:
    ticker = "NVDA"
    path = "v7/finance/options"
    session = MockSession()
    url = f"{GetTickerDataTask._BASE_URL}/{path}/{ticker}"

    session.add(url, "GET", mock_options)

    task = GetTickerDataTask(path=path, ticker=ticker).run(session=cast(ClientSession, session))

    options = await task

    assert options == mock_options
