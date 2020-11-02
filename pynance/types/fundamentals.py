from typing import TypedDict


class ReportedValueDict(TypedDict):

    raw: float
    fmt: str


class FundamentalsRowDict(TypedDict):

    dataId: int
    asOfDate: str
    periodType: str
    reportedValue: ReportedValueDict
    currencyCode: str


class FundamentalsMetaDict(TypedDict):

    symbol: str
    type: str


class FundamentalsDataRowDict(FundamentalsMetaDict):

    dataId: int
    asOfDate: str
    periodType: str
    reportedValue: float
    currencyCode: str
