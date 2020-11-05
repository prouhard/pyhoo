import abc
from typing import Any, List


class BaseParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abc.abstractmethod
    def to_records(self) -> List[Any]:
        pass

    def __repr__(self) -> str:
        formatted_attrs = ", ".join(
            attr_name + "=" + attr_value.__repr__() for attr_name, attr_value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({formatted_attrs})"
