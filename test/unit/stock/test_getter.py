import json

import pytest

from pynance.models.stock import Interval
from pynance.stock.getter import GetTickerStockTask

with open("test/unit/responses/stock.json", "r") as file:
    mock_stock = json.load(file)


from test.mock.session import MockSession


@pytest.mark.asyncio
async def test_getter_run() -> None:
    ticker = "NVDA"
    start_timestamp = 1594647000
    end_timestamp = 1594992600
    interval = Interval.ONE_DAY
    session = MockSession()
    url = (
        f"{GetTickerStockTask._BASE_URL}/v8/finance/chart/{ticker}?"
        f"period1={start_timestamp}&"
        f"period2={end_timestamp}&"
        f"interval={interval.value}"
    )

    session.add(url, "GET", mock_stock)

    task = GetTickerStockTask(
        ticker=ticker,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        interval=interval,
    ).run(session=session)

    stock = await task
    assert len(stock) == 1
