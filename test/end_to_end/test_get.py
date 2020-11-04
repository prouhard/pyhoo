import json
from typing import cast
from unittest.mock import MagicMock, patch

from aiohttp import ClientSession

from pynance import get
from test.mock.session import MockSession

with open("test/unit/responses/chart.json", "r") as file:
    mock_chart = json.load(file)

with open("test/unit/responses/fundamentals.json", "r") as file:
    mock_fundamentals = json.load(file)

with open("test/unit/responses/options.json", "r") as file:
    mock_options = json.load(file)


BASE_URL = "https://query2.finance.yahoo.com"


@patch("pynance.requester.aiohttp.ClientSession")
def test_get_chart(client_session_mock: MagicMock) -> None:

    url = "https://query2.finance.yahoo.com/v8/finance/chart/NVDA?period1=1601503200&period2=1602108000&interval=1d"

    session = cast(ClientSession, MockSession())
    client_session_mock.return_value = session

    session.add(url, "GET", mock_chart)

    chart_data = get(
        endpoint="chart",
        tickers=["NVDA"],
        start="2020-10-01",
        end="2020-10-08",
        granularity="1d",
    )

    assert len(chart_data) == 5


@patch("pynance.requester.aiohttp.ClientSession")
def test_get_fundamentals(client_session_mock: MagicMock) -> None:

    url = (
        "https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/NVDA"
        "?period1=1601503200&period2=1602108000&type=annualWorkInProcess,annualConstructionInProgress"
    )

    session = cast(ClientSession, MockSession())
    client_session_mock.return_value = session

    session.add(url, "GET", mock_fundamentals)

    fundamentals_data = get(
        endpoint="fundamentals",
        tickers=["NVDA"],
        start="2020-10-01",
        end="2020-10-08",
        type=["annualWorkInProcess", "annualConstructionInProgress"],
    )

    assert len(fundamentals_data) == 4


@patch("pynance.requester.aiohttp.ClientSession")
def test_get_options(client_session_mock: MagicMock) -> None:

    url = "https://query2.finance.yahoo.com/v7/finance/options/NVDA"

    session = cast(ClientSession, MockSession())
    client_session_mock.return_value = session

    session.add(url, "GET", mock_options)

    options_data = get(endpoint="options", tickers=["NVDA"])

    assert len(options_data) == 3
