from typing import Dict, Iterable, List, Optional

from pyhoo.models.fundamentals import FundamentalsMeta, FundamentalsRow
from pyhoo.models.iterables import Timestamp
from pyhoo.parsers.abc import BaseParser
from pyhoo.types.fundamentals import (
    FundamentalsDataRowDict,
    FundamentalsMetaDict,
    FundamentalsRowDict,
)


class FundamentalsParser(BaseParser):
    def __init__(
        self,
        meta: FundamentalsMetaDict,
        timestamp: Optional[List[int]] = None,
        **data: Iterable[FundamentalsRowDict],
    ) -> None:
        self.meta = FundamentalsMeta(**meta)
        self.timestamp = Timestamp(timestamp or [])
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
