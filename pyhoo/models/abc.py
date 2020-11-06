import abc
from dataclasses import dataclass
from typing import Any, Optional


class BaseModel(metaclass=abc.ABCMeta):
    """Base class for API response sub keys.
    Provide a user friendly `__repr__` method.
    """

    def __repr__(self) -> str:
        formatted_attrs = ", ".join(
            attr_name + "=" + attr_value.__repr__() for attr_name, attr_value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({formatted_attrs})"


@dataclass(frozen=True)
class OptionalFieldsModel(BaseModel):
    """For pure dataclasses without custom `__init__` method.
    Make all fields optional and default to `None`.
    It allows for less verbose dataclass declaration.
    """

    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        for field, value in cls.__annotations__.items():
            cls.__annotations__[field] = Optional[value]
            if not hasattr(cls, field):
                setattr(cls, field, None)
        super().__init_subclass__(*args, **kwargs)  # type: ignore
