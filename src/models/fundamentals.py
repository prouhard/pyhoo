import attr
import enum

from typing import Any, Dict, List
from models.iterables import Timestamp


class Frequency(enum.Enum):
    ANNUAL = 'annual'
    QUARTERLY = 'quarterly'
    MONTHLY = 'monthly'


@attr.s(slots=True)
class ReportedValue:
    raw: float = attr.ib()
    fmt: str = attr.ib()


@attr.s(slots=True)
class Row:
    dataId: int = attr.ib()
    asOfDate: str = attr.ib()
    periodType: str = attr.ib()
    reportedValue: ReportedValue = attr.ib(converter=lambda reported_value: ReportedValue(**reported_value))
    currencyCode: str = attr.ib(default='')


@attr.s(slots=True)
class FundamentalsMeta:
    symbol: str = attr.ib(converter=lambda symbol: symbol[0])
    type: str = attr.ib(converter=lambda type: type[0])


class FundamentalsData:
    def __init__(
        self,
        meta: Dict[str, Any],
        timestamp: List[int] = [],
        **data: List[Dict[str, Any]]
    ) -> None:
        self.meta = FundamentalsMeta(**meta)
        self.timestamp = Timestamp(timestamp)
        self._parse_data(data)

    def _parse_data(self, data: List[Dict[str, Any]]) -> List[Row]:
        fundamentals_name = self.meta.type
        fundamentals_data = next(iter(data.values())) if data else []
        setattr(self, fundamentals_name, [Row(**row) for row in fundamentals_data])

    def has_data(self) -> bool:
        return len(getattr(self, self.meta.type[0])) > 0

    def to_records(self) -> Dict[str, Any]:
        return [
            {
                'type': self.meta.type,
                'symbol': self.meta.symbol,
                'dataId': row.dataId,
                'asOfDate': row.asOfDate,
                'periodType': row.periodType,
                'reportedValue': row.reportedValue.raw,
                'currencyCode': row.currencyCode,
            }
            for row in getattr(self, self.meta.type)
        ]

    def __repr__(self) -> str:
        formatted_attrs = ', '.join(
            attr_name + '=' + attr_value.__repr__()
            for attr_name, attr_value in self.__dict__.items()
        )
        return f'{self.__class__.__name__}({formatted_attrs})'
