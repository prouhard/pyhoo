from typing import Iterable, TypedDict


class OptionDict(TypedDict):

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


class OptionQuoteDictBase(TypedDict):

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


class OptionQuoteDict(OptionQuoteDictBase, total=False):
    preMarketChange: float
    preMarketChangePercent: float
    preMarketTime: float
    preMarketPrice: float


class OptionsDict(TypedDict):

    expirationDate: int
    hasMiniOptions: bool
    calls: Iterable[OptionDict]
    puts: Iterable[OptionDict]


class OptionsDataRecord(OptionDict):
    underlyingSymbol: str
    type: str
