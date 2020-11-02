import enum
from typing import Dict, Iterable, List, Sequence, TypeVar

from pynance.models.abc import BaseModel
from pynance.models.iterables import Timestamp
from pynance.types.fundamentals import (
    FundamentalsDataRowDict,
    FundamentalsMetaDict,
    FundamentalsRowDict,
    ReportedValueDict,
)

T = TypeVar("T")


class Frequency(enum.Enum):

    ANNUAL = "annual"
    QUARTERLY = "quarterly"
    MONTHLY = "monthly"


class ReportedValue(BaseModel):

    raw: float
    fmt: str

    def __init__(self, raw: float, fmt: str) -> None:
        self.raw = raw
        self.fmt = fmt


class FundamentalsRow(BaseModel):

    dataId: int
    asOfDate: str
    periodType: str
    reportedValue: ReportedValue
    currencyCode: str

    def __init__(
        self,
        dataId: int,
        asOfDate: str,
        periodType: str,
        reportedValue: ReportedValueDict,
        currencyCode: str = "",
    ) -> None:
        self.dataId = dataId
        self.asOfDate = asOfDate
        self.periodType = periodType
        self.reportedValue = ReportedValue(**reportedValue)
        self.currencyCode = currencyCode


class FundamentalsMeta(BaseModel):

    symbol: str
    type: str

    def __init__(self, symbol: Sequence[str], type: Sequence[str]) -> None:
        self.symbol = self._get_first_element(symbol)
        self.type = self._get_first_element(type)

    @staticmethod
    def _get_first_element(sequence: Sequence[T]) -> T:
        return sequence[0]


class FundamentalsData(BaseModel):
    def __init__(
        self,
        meta: FundamentalsMetaDict,
        timestamp: Iterable[int],
        **data: Iterable[FundamentalsRowDict],
    ) -> None:
        self.meta = FundamentalsMeta(**meta)
        self.timestamp = Timestamp(timestamp)
        self._parse_data(data)

    def _parse_data(self, data: Dict[str, Iterable[FundamentalsRowDict]]) -> None:
        fundamentals_name = self.meta.type
        fundamentals_data = next(iter(data.values())) if data else []
        setattr(
            self,
            fundamentals_name,
            [FundamentalsRow(**row) for row in fundamentals_data],
        )

    def to_records(self) -> List[FundamentalsDataRowDict]:
        return [
            {
                "type": self.meta.type,
                "symbol": self.meta.symbol,
                "dataId": row.dataId,
                "asOfDate": row.asOfDate,
                "periodType": row.periodType,
                "reportedValue": row.reportedValue.raw,
                "currencyCode": row.currencyCode,
            }
            for row in getattr(self, self.meta.type)
        ]

    def __repr__(self) -> str:
        formatted_attrs = ", ".join(
            attr_name + "=" + attr_value.__repr__() for attr_name, attr_value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({formatted_attrs})"
