import asyncio
from typing import Any, Dict, Iterable, Type, Union, cast

import pandas as pd

from pyhoo.config import endpoints_config
from pyhoo.parsers.abc import BaseParser
from pyhoo.requester import Requester
from pyhoo.types import ApiResponse, Endpoint


def get(
    endpoint: Endpoint,
    tickers: Union[str, Iterable[str]],
    max_concurrent_calls: int = 100,
    **params: Any,
) -> pd.DataFrame:
    if not _is_iterable(tickers):
        tickers = [cast(str, tickers)]
    endpoint_config = endpoints_config[endpoint]
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


def _is_iterable(obj: Any) -> bool:
    """Check that an object is iterable but not a string (strings are iterable)."""
    return hasattr(obj, "__iter__") and not isinstance(obj, str)


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
