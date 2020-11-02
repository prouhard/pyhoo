import json
from unittest.mock import PropertyMock, patch

import pytest

from pynance.fundamentals.getter import GetTickerFundamentalsTask
from pynance.models.fundamentals import Frequency

with open('test/unit/responses/fundamentals.json', 'r') as file:
    mock_fundamentals = json.load(file)


from test.mock.session import MockSession


@pytest.mark.asyncio
@patch.object(GetTickerFundamentalsTask, '_types', new_callable=PropertyMock)
async def test_hello(mock_types: PropertyMock) -> None:
    ticker = 'NVDA'
    start_timestamp = 1485820800
    end_timestamp = 1517356800
    types = 'annualWorkInProcess,annualConstructionInProgress'
    mock_types.return_value = types
    session = MockSession()
    url = (
        f'{GetTickerFundamentalsTask._BASE_URL}/{ticker}?'
        f'period1={start_timestamp}&'
        f'period2={end_timestamp}&'
        f'type={types}'
    )
    session.add(url, 'GET', mock_fundamentals)

    task = GetTickerFundamentalsTask(
        ticker=ticker,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        frequency=Frequency.ANNUAL
    ).run(session=session)

    fundamentals = await task
    assert len(fundamentals) == 2
