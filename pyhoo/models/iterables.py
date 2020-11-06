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

T = TypeVar("T")


class CustomIterable(BaseModel, Generic[T]):

    _values: List[T]

    def __init__(self, values: List[T]) -> None:
        self._values = values

    def __iter__(self) -> "CustomIterator[T]":
        return CustomIterator(self)

    def __getitem__(self, index: int) -> T:
        return self._values[index]

    def __len__(self) -> int:
        return len(self._values)


class CustomIterator(Generic[T]):

    _iterable: CustomIterable[T]
    _index: int

    def __init__(self, iterable: CustomIterable[T]) -> None:
        self._iterable = iterable
        self._index = 0

    def __next__(self) -> T:
        if self._index < len(self._iterable):
            result = self._iterable[self._index]
            self._index += 1
            return result
        raise StopIteration

    def __iter__(self) -> CustomIterator[T]:
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
