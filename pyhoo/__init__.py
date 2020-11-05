import asyncio
from typing import Any, Dict, Iterable, Type, Union, cast

import pandas as pd

from pyhoo.config import endpoints_config
from pyhoo.errors import ApiError
from pyhoo.parsers.abc import BaseParser
from pyhoo.requester import Requester
from pyhoo.types import ApiResponse, Endpoint, ErrorDescription


def get(
    endpoint: Endpoint,
    tickers: Union[str, Iterable[str]],
    max_concurrent_calls: int = 100,
    ignore_errors: bool = False,
    **params: Any,
) -> pd.DataFrame:
    if not _is_iterable(tickers):
        tickers = [cast(str, tickers)]
    endpoint_config = endpoints_config[endpoint]
    endpoint_config.validate(params)
    responses = asyncio.run(
        Requester(
            path=endpoint_config.path,
            tickers=tickers,
            max_concurrent_calls=max_concurrent_calls,
            **endpoint_config.format(params),
        ).request()
    )
    return _convert_to_dataframe(
        responses=responses,
        response_field=endpoint_config.response_field,
        parser=endpoint_config.parser,
        ignore_errors=ignore_errors,
    )


def _is_iterable(obj: Any) -> bool:
    """Check that an object is iterable but not a string (strings are iterable)."""
    return hasattr(obj, "__iter__") and not isinstance(obj, str)


def _convert_to_dataframe(
    responses: Iterable[Dict[str, ApiResponse]],
    response_field: str,
    parser: Type[BaseParser],
    ignore_errors: bool,
) -> pd.DataFrame:
    records = []
    for response in responses:
        response_data = response[response_field]
        if response_data.get("error") is not None:
            if ignore_errors:
                continue
            error = cast(ErrorDescription, response_data["error"])
            raise ApiError(error["code"], error["description"])
        result = response_data["result"]
        if result is not None:
            records += [record for data in result for record in parser(**data).to_records()]
    return pd.DataFrame(records)
