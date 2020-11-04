from dataclasses import dataclass, field
from typing import Iterable

from pyhoo.models.abc import BaseModel
from pyhoo.types.options import OptionDict


@dataclass
class Option:

    contractSymbol: str
    strike: float
    currency: str
    lastPrice: float
    change: float
    percentChange: float
    ask: float
    contractSize: str
    expiration: int
    lastTradeDate: int
    impliedVolatility: float
    inTheMoney: bool
    volume: int = field(default=0)
    bid: float = field(default=0.0)
    openInterest: int = field(default=0)


@dataclass
class OptionQuote:

    language: str
    region: str
    quoteType: str
    quoteSourceName: str
    triggerable: bool
    currency: str
    sharesOutstanding: int
    bookValue: float
    fiftyDayAverage: float
    fiftyDayAverageChange: float
    fiftyDayAverageChangePercent: float
    twoHundredDayAverage: float
    twoHundredDayAverageChange: float
    twoHundredDayAverageChangePercent: float
    marketCap: int
    forwardPE: float
    priceToBook: float
    sourceInterval: int
    exchangeDataDelayedBy: int
    tradeable: bool
    ask: float
    bidSize: int
    askSize: int
    fullExchangeName: str
    financialCurrency: str
    regularMarketOpen: float
    averageDailyVolume3Month: int
    averageDailyVolume10Day: int
    fiftyTwoWeekLowChange: float
    fiftyTwoWeekLowChangePercent: float
    fiftyTwoWeekRange: str
    fiftyTwoWeekHighChange: float
    fiftyTwoWeekHighChangePercent: float
    fiftyTwoWeekLow: float
    fiftyTwoWeekHigh: float
    dividendDate: int
    earningsTimestamp: int
    earningsTimestampStart: int
    earningsTimestampEnd: int
    trailingAnnualDividendRate: float
    trailingPE: float
    trailingAnnualDividendYield: float
    epsTrailingTwelveMonths: float
    epsForward: float
    epsCurrentYear: float
    priceEpsCurrentYear: float
    exchange: str
    shortName: str
    longName: str
    messageBoardId: str
    exchangeTimezoneName: str
    exchangeTimezoneShortName: str
    gmtOffSetMilliseconds: int
    market: str
    esgPopulated: bool
    marketState: str
    firstTradeDateMilliseconds: int
    priceHint: int
    regularMarketChange: float
    regularMarketChangePercent: float
    regularMarketTime: float
    regularMarketPrice: float
    regularMarketDayHigh: float
    regularMarketDayRange: str
    regularMarketDayLow: float
    regularMarketVolume: int
    regularMarketPreviousClose: float
    bid: float
    displayName: str
    symbol: str
    preMarketChange: float = field(default=0.0)
    preMarketChangePercent: float = field(default=0.0)
    preMarketTime: float = field(default=0.0)
    preMarketPrice: float = field(default=0.0)


class Options(BaseModel):

    expirationDate: int
    hasMiniOptions: bool
    calls: Iterable[Option]
    puts: Iterable[Option]

    def __init__(
        self, expirationDate: int, hasMiniOptions: bool, calls: Iterable[OptionDict], puts: Iterable[OptionDict]
    ) -> None:
        self.expirationDate = expirationDate
        self.hasMiniOptions = hasMiniOptions
        self.calls = [Option(**call) for call in calls]
        self.puts = [Option(**put) for put in puts]
