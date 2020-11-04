from typing import List, TypedDict


class QuoteDict(TypedDict):

    high: List[float]
    volume: List[float]
    open: List[float]
    close: List[float]
    low: List[float]


class AdjCloseDict(TypedDict):

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
    range: str


class ChartMetaDict(ChartMetaDictBase):

    currentTradingPeriod: CurrentTradingPeriodDict
    validRanges: List[str]


class ChartDataRecord(TypedDict):
    timestamp: int
    high: float
    low: float
    volume: float
    open: float
    close: float
    adjclose: float
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
    range: str
