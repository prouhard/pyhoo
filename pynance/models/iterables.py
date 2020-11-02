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

import attr

T = TypeVar('T')


@attr.s
class CustomIterable(Generic[T]):

    _values: List[T] = attr.ib(factory=list)

    def __iter__(self) -> 'CustomIterator[T]':
        return CustomIterator(self)

    def __getitem__(self, index: int) -> T:
        return self._values[index]

    def __len__(self) -> int:
        return len(self._values)

    def __add__(self, custom_iterable: CustomIterable[T]) -> CustomIterable[T]:
        return self.__class__(self._values + custom_iterable._values)


@attr.s
class CustomIterator(Generic[T]):

    _custom_iterable: CustomIterable[T] = attr.ib()
    _index: int = 0

    def __next__(self) -> T:
        if self._index < len(self._custom_iterable):
            result = self._custom_iterable[self._index]
            self._index += 1
            return result
        raise StopIteration

    def __iter__(self) -> CustomIterator[T]:
        return self


class Timestamp(CustomIterable[int]):

    def to_str(self, format: str = '%Y-%m-%dT%H:%M:%S') -> List[str]:
        """Convert each timestamp to a datetime object and then format it as specified."""
        return list(map(lambda date: date.strftime(format), self.to_datetime()))

    def to_datetime(self) -> List[datetime.datetime]:
        """Convert each timestamp to a datetime object."""
        return list(map(datetime.datetime.fromtimestamp, self))