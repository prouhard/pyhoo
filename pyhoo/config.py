import datetime
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from pyhoo.errors import (
    InvalidParameterPrefixError,
    InvalidParameterTypeError,
    InvalidParameterValueError,
    MissingParameterError,
    UnknownParameterError,
)
from pyhoo.parsers import ChartParser, FundamentalsParser, OptionsParser
from pyhoo.parsers.abc import BaseParser

_T = TypeVar("_T")
_V = TypeVar("_V")

FUNDAMENTALS_TYPE_OPTIONS_PATH = Path(__file__).parent / "data/fundamentals_type_options.txt"


class ParamConfig:
    def __init__(
        self,
        name: str,
        api_name: str,
        type: Type[_T],
        required: bool = False,
        converter: Optional[Callable[[_T], _V]] = None,
        default: Optional[Any] = None,
        options: Optional[Iterable[_T]] = None,
        prefixes: Optional[Iterable[str]] = None,
    ) -> None:
        self.name = name
        self.api_name = api_name
        self.type = type
        self.converter = converter
        self.default = default
        self.required = required
        self.options = {option for option in options or []}
        self.prefixes = prefixes or []

    def validate(self, value: _T) -> None:
        if not isinstance(value, self.type):
            raise InvalidParameterTypeError(self.name, type(value), self.type)
        if self.options:
            values = cast(Iterable[_T], [value] if self.type != list else value)
            for _value in values:
                unprefixed_value = self._unprefix(cast(str, _value))
                if unprefixed_value not in self.options:
                    raise InvalidParameterValueError(self.name, unprefixed_value, self.options)

    def format(self, value: _T) -> Union[_T, _V]:
        if self.converter:
            return self.converter(value)
        return value

    def _unprefix(self, value: str) -> Optional[str]:
        """Remove the longest found prefix (in `self.prefixes`) from value.
        Currently used to check fundamentals types options.
        """
        if self.prefixes:
            # We need to match the 'un-prefixed' value against the allowed options
            prefix_lengths = [len(prefix) for prefix in self.prefixes if value.startswith(prefix)]
            if prefix_lengths:
                # We match the longest prefix
                return value[max(prefix_lengths) :]
            else:
                raise InvalidParameterPrefixError(self.name, value, self.prefixes)
        return value


class Config:
    def __init__(
        self,
        path: str,
        response_field: str,
        parser: Type[BaseParser],
        params_config: Iterable[ParamConfig],
    ) -> None:
        self.path = path
        self.response_field = response_field
        self.parser = parser
        self.params_config = {param.name: param for param in params_config}

    def validate(self, params: Dict[str, Any]) -> None:
        for param, value in params.items():
            param_config = self.params_config.get(param)
            if param_config is None:
                raise UnknownParameterError(param, self.params_config)
            param_config.validate(value)
        for param, param_config in self.params_config.items():
            if param_config.required and param not in params:
                if param_config.default is not None:
                    params[param] = param_config.default
                else:
                    raise MissingParameterError(param)

    def format(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            self.params_config[param].api_name: self.params_config[param].format(value)
            for param, value in params.items()
        }


def str_date_to_timestamp(str_date: str) -> int:
    return int(datetime.datetime.timestamp(datetime.datetime.strptime(str_date, "%Y-%m-%d")))


with open(FUNDAMENTALS_TYPE_OPTIONS_PATH, "r") as file:
    fundamentals_type_options = [line.strip() for line in file.readlines()]


endpoints_config = {
    "chart": Config(
        path="v8/finance/chart",
        response_field="chart",
        parser=ChartParser,
        params_config=[
            ParamConfig(
                name="start",
                api_name="period1",
                type=str,
                required=True,
                converter=str_date_to_timestamp,
            ),
            ParamConfig(
                name="end",
                api_name="period2",
                type=str,
                required=True,
                converter=str_date_to_timestamp,
            ),
            ParamConfig(
                name="granularity",
                api_name="interval",
                type=str,
                required=True,
                default="1d",
                options=["1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1w", "1mo", "3mo"],
            ),
            ParamConfig(
                name="range",
                api_name="range",
                type=str,
                required=False,
                options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
            ),
        ],
    ),
    "fundamentals": Config(
        path="ws/fundamentals-timeseries/v1/finance/timeseries",
        response_field="timeseries",
        parser=FundamentalsParser,
        params_config=[
            ParamConfig(
                name="start",
                api_name="period1",
                type=str,
                required=False,
                converter=str_date_to_timestamp,
            ),
            ParamConfig(
                name="end",
                api_name="period2",
                type=str,
                required=False,
                converter=str_date_to_timestamp,
            ),
            ParamConfig(
                name="type",
                api_name="type",
                type=list,
                required=True,
                options=fundamentals_type_options,
                default=[f"annual{value}" for value in fundamentals_type_options],
                converter=lambda values: ",".join(values),
                prefixes=["monthly", "quarterly", "annual"],
            ),
        ],
    ),
    "options": Config(
        path="v7/finance/options",
        response_field="optionChain",
        parser=OptionsParser,
        params_config=[
            ParamConfig(
                name="start",
                api_name="date",
                type=str,
                required=False,
                converter=str_date_to_timestamp,
            ),
            ParamConfig(
                name="end",
                api_name="endDate",
                type=str,
                required=False,
                converter=str_date_to_timestamp,
            ),
            ParamConfig(
                name="strikeMin",
                api_name="strikeMin",
                type=float,
                required=False,
            ),
            ParamConfig(
                name="strikeMax",
                api_name="strikeMax",
                type=float,
                required=False,
            ),
        ],
    ),
}
