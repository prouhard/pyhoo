from dataclasses import dataclass
from typing import Iterable, Optional

from pyhoo.models.abc import BaseModel, OptionalFieldsModel
from pyhoo.types.options import OptionDict


@dataclass(frozen=True)
class Option(OptionalFieldsModel):

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
    volume: int
    bid: float
    openInterest: int


@dataclass(frozen=True)
class OptionQuote(OptionalFieldsModel):

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
    preMarketChange: float
    preMarketChangePercent: float
    preMarketTime: float
    preMarketPrice: float
    dividendDate: int


class Options(BaseModel):

    expirationDate: Optional[int]
    hasMiniOptions: Optional[bool]
    calls: Iterable[Option]
    puts: Iterable[Option]

    def __init__(
        self,
        expirationDate: Optional[int] = None,
        hasMiniOptions: Optional[bool] = None,
        calls: Optional[Iterable[OptionDict]] = None,
        puts: Optional[Iterable[OptionDict]] = None,
    ) -> None:
        self.expirationDate = expirationDate
        self.hasMiniOptions = hasMiniOptions
        self.calls = [Option(**call) for call in calls or []]
        self.puts = [Option(**put) for put in puts or []]
