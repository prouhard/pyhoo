from typing import Any, Iterable


class CustomException(Exception):
    pass


class UnknownParameterError(CustomException):
    def __init__(self, param: str, valid_params: Iterable[str]) -> None:
        super().__init__(f"Expected one of {[param for param in valid_params]}, got '{param}'.")


class InvalidParameterValueError(CustomException):
    def __init__(self, param: str, value: Any, options: Iterable[Any]) -> None:
        super().__init__(f"'{param}' has invalid value '{value}', must be one of {[option for option in options]}.")


class InvalidParameterTypeError(CustomException):
    def __init__(self, param: str, param_type: Any, config_type: Any) -> None:
        super().__init__(f"'{param}' has invalid type '{param_type}', expected {config_type}.")


class InvalidParameterPrefixError(CustomException):
    def __init__(self, param: str, value: Any, prefixes: Iterable[str]) -> None:
        super().__init__(f"'{param}' has invalid prefix, it must starts with one of {prefixes}.")


class MissingParameterError(CustomException):
    def __init__(self, param: str) -> None:
        super().__init__(f"Missing parameter '{param}'.")


class ApiError(CustomException):
    def __init__(self, code: str, description: str) -> None:
        super().__init__(f"Got error '{code}' from Yahoo Finance API, reason was: '{description}'")
