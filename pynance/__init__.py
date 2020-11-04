import asyncio
from typing import Any, Dict, Iterable, Type

import pandas as pd

from pynance.config import config
from pynance.parsers.abc import BaseParser
from pynance.requester import Requester
from pynance.types import ApiResponse, Endpoint


def get(
    endpoint: Endpoint,
    tickers: Iterable[str],
    max_concurrent_calls: int = 100,
    **params: Any,
) -> pd.DataFrame:
    endpoint_config = config[endpoint]
    endpoint_config.validate(params)
    batch_tickers_data = asyncio.run(
        Requester(
            path=endpoint_config.path,
            tickers=tickers,
            max_concurrent_calls=max_concurrent_calls,
            **endpoint_config.format(params),
        ).request()
    )
    return _convert_to_dataframe(
        data=batch_tickers_data,
        response_field=endpoint_config.response_field,
        parser=endpoint_config.parser,
    )


def _convert_to_dataframe(
    data: Iterable[Dict[str, ApiResponse]],
    response_field: str,
    parser: Type[BaseParser],
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            record
            for raw_responses in data
            for ticker_data in [parser(**response) for response in raw_responses[response_field]["result"]]
            for record in ticker_data.to_records()
        ],
    )
