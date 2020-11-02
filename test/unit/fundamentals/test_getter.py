import json
from unittest.mock import patch

from aiohttp import web

from src.fundamentals.getter import GetTickerFundamentalsTask
from src.models.fundamentals import Frequency

with open('test/unit/responses/fundamentals.json', 'r') as file:
    mock_fundamentals = json.load(file)


async def fundamentals(request):
    return web.Response(body=json.dumps(mock_fundamentals))


def mock_yahoo_finance_api(loop):
    app = web.Application(loop=loop)

    ticker = 'NVDA'
    start_timestamp = 1485820800
    end_timestamp = 1517356800
    types = 'annualWorkInProcess,annualConstructionInProgress'

    app.router.add_route(
        'GET',
        (
            f'{GetTickerFundamentalsTask._BASE_URL}/{ticker}?'
            f'period1={start_timestamp}&'
            f'period2={end_timestamp}&'
            f'type={types}'
        ),
        fundamentals,
    )
    return app


@patch.object(GetTickerFundamentalsTask, '_types')
async def test_hello(mock_types, test_client):
    client = await test_client(mock_yahoo_finance_api)
    ticker = 'NVDA'
    start_timestamp = 1485820800
    end_timestamp = 1517356800
    mock_types.return_value = 'annualWorkInProcess,annualConstructionInProgress'
    resp = GetTickerFundamentalsTask(
        ticker=ticker,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        frequency=Frequency.ANNUAL
    ).run(session=client)
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text
