from dataclasses import dataclass
from typing import Optional, Sequence, TypeVar

from pyhoo.models.abc import BaseModel, OptionalFieldsModel
from pyhoo.types.fundamentals import ReportedValueDict


@dataclass(frozen=True)
class ReportedValue(OptionalFieldsModel):

    raw: float
    fmt: str


class FundamentalsRow(BaseModel):

    dataId: int
    asOfDate: str
    periodType: str
    reportedValue: ReportedValue
    currencyCode: Optional[str]

    def __init__(
        self,
        dataId: int,
        asOfDate: str,
        periodType: str,
        reportedValue: ReportedValueDict,
        currencyCode: Optional[str] = None,
    ) -> None:
        self.dataId = dataId
        self.asOfDate = asOfDate
        self.periodType = periodType
        self.reportedValue = ReportedValue(**reportedValue)
        self.currencyCode = currencyCode


_T = TypeVar("_T")


class FundamentalsMeta(BaseModel):

    symbol: str
    type: str

    def __init__(self, symbol: Sequence[str], type: Sequence[str]) -> None:
        self.symbol = self._get_first_element(symbol)
        self.type = self._get_first_element(type)

    @staticmethod
    def _get_first_element(sequence: Sequence[_T]) -> _T:
        return sequence[0]
