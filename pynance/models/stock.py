from __future__ import annotations

import enum
from typing import Iterable, List, Optional

from pynance.models.abc import BaseModel
from pynance.models.iterables import Timestamp
from pynance.types.stock import (
    CurrentTradingPeriodDict,
    IndicatorsDict,
    StockDataRecord,
    StockMetaDict,
    TradingPeriodDict,
)


class Interval(enum.Enum):

    ONE_MIN = "1m"
    TWO_MIN = "2m"
    FIVE_MIN = "5m"
    FIFTEEN_MIN = "15m"
    THIRTY_MIN = "30m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"

    def is_intraday(self) -> bool:
        return self in {
            Interval.ONE_MIN,
            Interval.TWO_MIN,
            Interval.FIVE_MIN,
            Interval.FIFTEEN_MIN,
            Interval.THIRTY_MIN,
            Interval.ONE_HOUR,
        }


class Quote(BaseModel):

    high: List[float]
    volume: List[float]
    open: List[float]
    close: List[float]
    low: List[float]

    def __init__(
        self,
        high: Optional[List[float]] = None,
        low: Optional[List[float]] = None,
        volume: Optional[List[float]] = None,
        open: Optional[List[float]] = None,
        close: Optional[List[float]] = None,
    ) -> None:
        self.high = high or []
        self.low = low or []
        self.volume = volume or []
        self.open = open or []
        self.close = close or []

    def __add__(self, quote: Quote) -> Quote:
        return Quote(
            **{attr: getattr(self, attr) + getattr(quote, attr) for attr in ["high", "low", "volume", "open", "close"]}
        )


class AdjClose(BaseModel):

    adjclose: List[float]

    def __init__(self, adjclose: Optional[List[float]] = None) -> None:
        self.adjclose = adjclose or []

    def __add__(self, adjclose: AdjClose) -> AdjClose:
        return AdjClose(self.adjclose + adjclose.adjclose)


class Indicators(BaseModel):

    quote: Quote
    adjclose: AdjClose

    def __init__(self, indicators: IndicatorsDict) -> Indicators:
        self.quote = Quote(**indicators["quote"][0])
        self.adjclose = AdjClose(**indicators["adjclose"][0])


class TradingPeriod(BaseModel):

    timezone: str
    start: int
    end: int
    gmtoffset: int

    def __init__(self, timezone: str, start: int, end: int, gmtoffset: int) -> None:
        self.timezone = timezone
        self.start = start
        self.end = end
        self.gmtoffset = gmtoffset


class CurrentTradingPeriod(BaseModel):

    pre: TradingPeriod
    regular: TradingPeriod
    post: TradingPeriod

    def __init__(self, pre: TradingPeriodDict, regular: TradingPeriodDict, post: TradingPeriodDict) -> None:
        self.pre = TradingPeriod(**pre)
        self.regular = TradingPeriod(**regular)
        self.post = TradingPeriod(**post)


class Range(enum.Enum):

    NONE = ""
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"
    SIX_MONTHS = "6mo"
    ONE_YEAR = "1y"
    TWO_YEARS = "2y"
    FIVE_YEARS = "5y"
    TEN_YEARS = "10y"
    YTD = "ytd"
    MAX = "max"


class StockMeta(BaseModel):

    currency: str
    symbol: str
    exchangeName: str
    instrumentType: str
    firstTradeDate: int
    regularMarketTime: int
    gmtoffset: int
    timezone: str
    exchangeTimezoneName: str
    regularMarketPrice: float
    chartPreviousClose: float
    priceHint: int
    currentTradingPeriod: CurrentTradingPeriod
    dataGranularity: Interval
    range: Range
    validRanges: List[Range]

    def __init__(
        self,
        currency: str,
        symbol: str,
        exchangeName: str,
        instrumentType: str,
        firstTradeDate: int,
        regularMarketTime: int,
        gmtoffset: int,
        timezone: str,
        exchangeTimezoneName: str,
        regularMarketPrice: float,
        chartPreviousClose: float,
        priceHint: int,
        currentTradingPeriod: CurrentTradingPeriodDict,
        dataGranularity: str,
        range: str,
        validRanges: List[str],
    ) -> None:
        self.currency = currency
        self.symbol = symbol
        self.exchangeName = exchangeName
        self.instrumentType = instrumentType
        self.firstTradeDate = firstTradeDate
        self.regularMarketTime = regularMarketTime
        self.gmtoffset = gmtoffset
        self.timezone = timezone
        self.exchangeTimezoneName = exchangeTimezoneName
        self.regularMarketPrice = regularMarketPrice
        self.chartPreviousClose = chartPreviousClose
        self.priceHint = priceHint
        self.currentTradingPeriod = CurrentTradingPeriod(**currentTradingPeriod)
        self.dataGranularity = Interval(dataGranularity)
        self.range = Range(range)
        self.validRanges = [Range(valid_range) for valid_range in validRanges]

    def to_dict(self) -> StockMetaDict:
        return {
            "currency": self.currency,
            "symbol": self.symbol,
            "exchangeName": self.exchangeName,
            "instrumentType": self.instrumentType,
            "firstTradeDate": self.firstTradeDate,
            "regularMarketTime": self.regularMarketTime,
            "gmtoffset": self.gmtoffset,
            "timezone": self.timezone,
            "exchangeTimezoneName": self.exchangeTimezoneName,
            "regularMarketPrice": self.regularMarketPrice,
            "chartPreviousClose": self.chartPreviousClose,
            "priceHint": self.priceHint,
            "dataGranularity": self.dataGranularity,
            "range": self.range,
        }


class StockData(BaseModel):

    meta: StockMeta
    timestamp: Timestamp
    indicators: Indicators

    def __init__(self, meta: StockMetaDict, timestamp: Iterable[int], indicators: IndicatorsDict) -> None:
        self.meta = StockMeta(**meta)
        self.timestamp = Timestamp(timestamp)
        self.indicators = Indicators(indicators)
        print(self.indicators)

    def to_records(self) -> List[StockDataRecord]:
        return [
            {
                "timestamp": timestamp,
                "high": high,
                "low": low,
                "volume": volume,
                "open": open,
                "close": close,
                "adjclose": adjclose,
                **self.meta.to_dict(),
            }
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
