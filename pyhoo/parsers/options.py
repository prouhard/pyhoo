from dataclasses import asdict
from typing import List, Sequence, cast

from pyhoo.models.iterables import Strikes, Timestamp
from pyhoo.models.options import OptionQuote, Options
from pyhoo.parsers.abc import BaseParser
from pyhoo.types.options import OptionQuoteDict, OptionsDataRecord, OptionsDict


class OptionsParser(BaseParser):

    underlyingSymbol: str
    expirationDates: Timestamp
    strikes: Strikes
    hasMiniOptions: bool
    quote: OptionQuote
    options: Options

    def __init__(
        self,
        underlyingSymbol: str,
        expirationDates: List[int],
        strikes: List[float],
        hasMiniOptions: bool,
        quote: OptionQuoteDict,
        options: Sequence[OptionsDict] = None,
    ) -> None:
        self.underlyingSymbol = underlyingSymbol
        self.expirationDates = Timestamp(expirationDates)
        self.strikes = Strikes(strikes)
        self.hasMiniOptions = hasMiniOptions
        self.quote = OptionQuote(**quote)
        self.options = Options(**options[0]) if options else Options()

    def to_records(self) -> List[OptionsDataRecord]:
        return [
            cast(
                OptionsDataRecord,
                {
                    "underlyingSymbol": self.underlyingSymbol,
                    "type": type,
                    **asdict(option),
                },
            )
            for option, type in [(call, "CALL") for call in self.options.calls]
            + [(put, "PUT") for put in self.options.puts]
        ]
