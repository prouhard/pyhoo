from dataclasses import asdict
from typing import List, Sequence, cast

from pynance.models.iterables import Strikes, Timestamp
from pynance.models.options import OptionQuote, Options
from pynance.parsers.abc import BaseParser
from pynance.types.options import (
    OptionQuoteDict,
    OptionsDataRecord,
    OptionsDict,
)


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
        options: Sequence[OptionsDict],
    ) -> None:
        self.underlyingSymbol = underlyingSymbol
        self.expirationDates = Timestamp(expirationDates)
        self.strikes = Strikes(strikes)
        self.hasMiniOptions = hasMiniOptions
        self.quote = OptionQuote(**quote)
        self.options = Options(**options[0])

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
