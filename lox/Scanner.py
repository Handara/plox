from Token import Token
from typing import Final,Self
import Lox

class Scanner:
    _source: Final[str] 
    _tokens: Final[list[Token]] = list()
    _start: int = 0
    _current: int = 0
    _line = 1

    def __init__(self: Self, source: str) -> None:
        self._source = source

    def scan_tokens(self) -> list[Token]:
        while(not is_at_end()):
            self._start = self._current
            Lox.scan_token()
        self._tokens.append(Token())
        return self._tokens

    def _isAtEnd(self) -> bool:
        return self._current > len(self._source) 