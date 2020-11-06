# TODO: Mutualize tests into a generic e2e test function with variable input / output

import json
from typing import cast
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
from aiohttp import ClientSession

from pyhoo import get
from pyhoo.config import fundamentals_type_options, str_date_to_timestamp
from tests.mock.session import MockSession


def _harmonize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by=df.columns.tolist()).reset_index(drop=True).fillna(value=np.nan).round(2)


@patch("pyhoo.requester.aiohttp.ClientSession")
def test_get_chart(client_session_mock: MagicMock) -> None:

    start = "2020-10-01"
    end = "2020-10-02"

    url = "https://query2.finance.yahoo.com/v8/finance/chart/NVDA"
    params = {
        "period1": str_date_to_timestamp(start),
        "period2": str_date_to_timestamp(end),
        "interval": "1h",
        "range": "1d",
    }

    with open("tests/end_to_end/inputs/chart_hourly.json", "r") as file:
        mock_chart = json.load(file)

    snapshot = pd.read_csv("tests/end_to_end/outputs/chart_hourly.csv")

    session = cast(ClientSession, MockSession())
    client_session_mock.return_value = session

    session.add(url, params, "GET", mock_chart)

    chart_data = get(
        endpoint="chart",
        tickers="NVDA",
        start=start,
        end=end,
        range="1d",
        granularity="1h",
    )

    assert _harmonize_dataframe(chart_data).equals(_harmonize_dataframe(snapshot))


@patch("pyhoo.requester.aiohttp.ClientSession")
def test_get_fundamentals(client_session_mock: MagicMock) -> None:

    start = "2020-01-01"
    end = "2020-12-31"

    url = "https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/AAPL"
    params = {
        "period1": str_date_to_timestamp(start),
        "period2": str_date_to_timestamp(end),
        "type": ",".join(f"annual{option}" for option in fundamentals_type_options),
    }

    with open("tests/end_to_end/inputs/fundamentals_annual.json", "r") as file:
        mock_chart = json.load(file)

    snapshot = pd.read_csv("tests/end_to_end/outputs/fundamentals_annual.csv")

    session = cast(ClientSession, MockSession())
    client_session_mock.return_value = session

    session.add(url, params, "GET", mock_chart)

    fundamentals_data = get(
        endpoint="fundamentals",
        tickers="AAPL",
        start=start,
        end=end,
    )

    assert _harmonize_dataframe(fundamentals_data).equals(_harmonize_dataframe(snapshot))


@patch("pyhoo.requester.aiohttp.ClientSession")
def test_get_options(client_session_mock: MagicMock) -> None:

    url = "https://query2.finance.yahoo.com/v7/finance/options/GOOGL"
    params = {"strikeMax": 400.0}

    with open("tests/end_to_end/inputs/options_strike_max.json", "r") as file:
        mock_options = json.load(file)

    snapshot = pd.read_csv("tests/end_to_end/outputs/options_strike_max.csv")

    session = cast(ClientSession, MockSession())
    client_session_mock.return_value = session

    session.add(url, params, "GET", mock_options)

    options_data = get(endpoint="options", tickers="GOOGL", strikeMax=400.0)

    assert _harmonize_dataframe(options_data).equals(_harmonize_dataframe(snapshot))
