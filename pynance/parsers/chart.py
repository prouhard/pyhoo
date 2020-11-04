from typing import List, cast

from pynance.models.iterables import Timestamp
from pynance.models.chart import Indicators, ChartMeta
from pynance.parsers.abc import BaseParser
from pynance.types.chart import IndicatorsDict, ChartDataRecord, ChartMetaDict


class ChartParser(BaseParser):

    meta: ChartMeta
    timestamp: Timestamp
    indicators: Indicators

    def __init__(self, meta: ChartMetaDict, timestamp: List[int], indicators: IndicatorsDict) -> None:
        self.meta = ChartMeta(**meta)
        self.timestamp = Timestamp(timestamp)
        self.indicators = Indicators(indicators)

    def to_records(self) -> List[ChartDataRecord]:
        return [
            cast(
                ChartDataRecord,
                {
                    "timestamp": timestamp,
                    "high": high,
                    "low": low,
                    "volume": volume,
                    "open": open,
                    "close": close,
                    "adjclose": adjclose,
                    **self.meta.to_dict(),
                },
            )
            for timestamp, high, low, volume, open, close, adjclose in zip(
                self.timestamp,
                self.indicators.quote.high,
                self.indicators.quote.low,
                self.indicators.quote.volume,
                self.indicators.quote.open,
                self.indicators.quote.close,
                self.indicators.adjclose.adjclose,
            )
        ]
