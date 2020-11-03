import json

import pytest

from pynance.options.getter import GetTickerOptionsTask

with open("test/unit/responses/options.json", "r") as file:
    mock_options = json.load(file)


from test.mock.session import MockSession


@pytest.mark.asyncio
async def test_getter_run() -> None:
    ticker = "NVDA"
    session = MockSession()
    url = f"{GetTickerOptionsTask._BASE_URL}/v7/finance/options/{ticker}"

    session.add(url, "GET", mock_options)

    task = GetTickerOptionsTask(ticker=ticker).run(session=session)

    options = await task
    assert len(options) == 1
