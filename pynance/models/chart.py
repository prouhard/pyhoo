from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import List, Optional

from pynance.models.abc import BaseModel
from pynance.types.chart import (
    CurrentTradingPeriodDict,
    IndicatorsDict,
    ChartMetaDictBase,
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


@dataclass
class Quote:

    high: List[float] = field(default_factory=list)
    volume: List[float] = field(default_factory=list)
    open: List[float] = field(default_factory=list)
    close: List[float] = field(default_factory=list)
    low: List[float] = field(default_factory=list)

    def __add__(self, quote: Quote) -> Quote:
        return Quote(
            **{attr: getattr(self, attr) + getattr(quote, attr) for attr in ["high", "low", "volume", "open", "close"]}
        )


@dataclass
class AdjClose(BaseModel):

    adjclose: List[float] = field(default_factory=list)

    def __add__(self, adjclose: AdjClose) -> AdjClose:
        return AdjClose(self.adjclose + adjclose.adjclose)


class Indicators(BaseModel):

    quote: Quote
    adjclose: AdjClose

    def __init__(self, indicators: IndicatorsDict) -> None:
        self.quote = Quote(**indicators["quote"][0])
        self.adjclose = AdjClose(**indicators["adjclose"][0])


@dataclass
class TradingPeriod:

    timezone: str
    start: int
    end: int
    gmtoffset: int


class CurrentTradingPeriod(BaseModel):

    pre: TradingPeriod
    regular: TradingPeriod
    post: TradingPeriod
    tradingPeriods: Optional[List[TradingPeriod]]

    def __init__(
        self,
        pre: TradingPeriodDict,
        regular: TradingPeriodDict,
        post: TradingPeriodDict,
        tradingPeriods: Optional[List[List[TradingPeriodDict]]] = None,
    ) -> None:
        self.pre = TradingPeriod(**pre)
        self.regular = TradingPeriod(**regular)
        self.post = TradingPeriod(**post)
        if tradingPeriods is not None:
            self.tradingPeriods = [TradingPeriod(**period) for periods in tradingPeriods for period in periods]


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


class ChartMeta(BaseModel):

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

    def to_dict(self) -> ChartMetaDictBase:
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
            "dataGranularity": self.dataGranularity.value,
            "range": self.range.value,
        }
