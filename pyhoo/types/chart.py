from typing import List, Optional, TypedDict


class QuoteDict(TypedDict, total=False):

    high: List[float]
    volume: List[float]
    open: List[float]
    close: List[float]
    low: List[float]


class AdjCloseDict(TypedDict, total=False):

    adjclose: List[float]


class IndicatorsDict(TypedDict):

    quote: List[QuoteDict]
    adjclose: List[AdjCloseDict]


class TradingPeriodDict(TypedDict):

    timezone: str
    start: int
    end: int
    gmtoffset: int


class CurrentTradingPeriodDict(TypedDict):

    pre: TradingPeriodDict
    regular: TradingPeriodDict
    post: TradingPeriodDict


class ChartMetaDictBase(TypedDict):

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
    dataGranularity: str
    range: Optional[str]
    scale: Optional[int]
    previousClose: Optional[float]


class ChartMetaDict(ChartMetaDictBase, total=False):

    currentTradingPeriod: CurrentTradingPeriodDict
    validRanges: List[str]
    tradingPeriods: List[List[TradingPeriodDict]]


class ChartDataRecord(ChartMetaDictBase):

    timestamp: int
    high: float
    low: float
    volume: float
    open: float
    close: float
    adjclose: float
