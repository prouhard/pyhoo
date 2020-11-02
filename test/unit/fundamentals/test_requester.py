import json
from unittest.mock import AsyncMock, patch

import pytest

from pynance.fundamentals.getter import GetTickerFundamentalsTask
from pynance.fundamentals.requester import TickerFundamentalsRequester
from pynance.models.fundamentals import Frequency, FundamentalsData

with open('test/unit/responses/fundamentals.json', 'r') as file:
    mock_fundamentals = json.load(file)


@pytest.mark.asyncio
@patch.object(GetTickerFundamentalsTask, 'run')
async def test_requester_request(mock_getter_run: AsyncMock) -> None:
    tickers = ['NVDA']
    start_timestamp = 1485820800
    end_timestamp = 1517356800
    frequency = Frequency.ANNUAL
    max_concurrent_calls = 1

    mock_getter_run.return_value = [
        FundamentalsData(**response)
        for response in mock_fundamentals['timeseries']['result']
    ]

    requester = TickerFundamentalsRequester(
        tickers=tickers,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        frequency=frequency,
        max_concurrent_calls=max_concurrent_calls,
    )

    fundamentals = await requester.request()

    assert fundamentals.columns.tolist() == [
        'type',
        'symbol',
        'dataId',
        'asOfDate',
        'periodType',
        'reportedValue',
        'currencyCode',
    ]

    assert len(fundamentals) == 4
