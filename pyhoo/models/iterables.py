"""
    Define a `CustomIterable[T]` generic type, to be used as an `attr.ib()`
    to parse sequences of any type with:
    `<ATTR_NAME>: CustomIterable = attr.ib(converter=CustomIterable)`.

    Ex:
        # Timestamp is defined below
        timestamp: Timestamp = attr.ib(converter=Timestamp)
"""
from __future__ import annotations

import datetime
from typing import Generic, List, TypeVar

from pyhoo.models.abc import BaseModel

_T = TypeVar("_T")


class CustomIterable(BaseModel, Generic[_T]):

    _values: List[_T]

    def __init__(self, values: List[_T]) -> None:
        self._values = values

    def __iter__(self) -> "CustomIterator[_T]":
        return CustomIterator(self)

    def __getitem__(self, index: int) -> _T:
        return self._values[index]

    def __len__(self) -> int:
        return len(self._values)


class CustomIterator(Generic[_T]):

    _iterable: CustomIterable[_T]
    _index: int

    def __init__(self, iterable: CustomIterable[_T]) -> None:
        self._iterable = iterable
        self._index = 0

    def __next__(self) -> _T:
        if self._index < len(self._iterable):
            result = self._iterable[self._index]
            self._index += 1
            return result
        raise StopIteration

    def __iter__(self) -> CustomIterator[_T]:
        return self


class Timestamp(CustomIterable[int]):
    def to_str(self, format: str = "%Y-%m-%dT%H:%M:%S") -> List[str]:
        """Convert each timestamp to a datetime object and then format it as specified."""
        return list(map(lambda date: date.strftime(format), self.to_datetime()))

    def to_datetime(self) -> List[datetime.datetime]:
        """Convert each timestamp to a datetime object."""
        return list(map(datetime.datetime.fromtimestamp, self))


class Strikes(CustomIterable[float]):
    pass
