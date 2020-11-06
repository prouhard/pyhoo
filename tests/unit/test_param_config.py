import pytest

from pyhoo.config import ParamConfig
from pyhoo.errors import (
    InvalidParameterPrefixError,
    InvalidParameterTypeError,
    InvalidParameterValueError,
)


def test_param_config_validate_raise_invalid_type() -> None:
    """ParamConfig type is `str`, passed value is `int`.
    It should raise an InvalidParameterTypeError.
    """
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=str,
        required=False,
    )

    with pytest.raises(InvalidParameterTypeError):
        param_config.validate(1)


def test_param_config_validate_raise_invalid_value() -> None:
    """Param value is not in ParamConfig options.
    It should raise an InvalidParameterValueError.
    """
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=str,
        required=False,
        options=["good_value_1", "good_value_2"],
    )

    with pytest.raises(InvalidParameterValueError):
        param_config.validate("bad_value")


def test_param_config_validate_raise_invalid_prefix() -> None:
    """Param value is prefixed with a prefix not in ParamConfig prefixes.
    It should raise an InvalidParameterPrefixError.
    """
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=str,
        required=False,
        options=["good_value_1", "good_value_2"],
        prefixes=["good_prefix_"],
    )

    with pytest.raises(InvalidParameterPrefixError):
        param_config.validate("bad_prefix_good_value_1")


def test_param_config_validate_ok_type() -> None:
    """It should not raise any error."""
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=str,
        required=False,
    )

    param_config.validate("param")


def test_param_config_validate_ok_type_options() -> None:
    """It should not raise any error."""
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=str,
        required=False,
        options=["good_value_1", "good_value_2"],
    )

    param_config.validate("good_value_1")
    param_config.validate("good_value_2")


def test_param_config_validate_ok_type_options_prefixes() -> None:
    """It should not raise any error."""
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=str,
        required=False,
        options=["good_value_1", "good_value_2"],
        prefixes=["good_prefix_1_", "good_prefix_2_"],
    )

    param_config.validate("good_prefix_1_good_value_1")
    param_config.validate("good_prefix_1_good_value_2")
    param_config.validate("good_prefix_2_good_value_1")
    param_config.validate("good_prefix_2_good_value_2")


def test_param_config_unprefix() -> None:
    """It should correctly remove the longest prefix of each string."""
    prefixed_strings = [
        "prefix_1_string",
        "prefix_2_string",
        "long_prefix_1_string",
        "long_prefix_2_string",
        "prefix_1_long_string",
        "prefix_2_long_string",
    ]
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=str,
        required=False,
        prefixes=[
            "prefix_1_",
            "prefix_2_",
            "long_prefix_1_",
            "long_prefix_2_",
            "prefix_1_long_",
            "prefix_2_long_",
        ],
    )
    for prefixed_string in prefixed_strings:
        assert param_config._unprefix(prefixed_string) == "string"


def test_param_config_format() -> None:
    """It should convert the values if there is a converter defined."""
    param_config = ParamConfig(
        name="name",
        api_name="api_name",
        type=int,
        required=False,
        converter=lambda value: -value,
    )

    assert param_config.format(1) == -1

    param_config.converter = None
    assert param_config.format(1) == 1
