"""The Token data type produced by the scanner."""

from typing import Final
from typing import Self

from .TokenType import TokenType

class Token:
    """A single lexeme plus everything the later stages need to know about it.

    Fields are annotated `Final` because a token never changes once the
    scanner has created it.
    """

    TYPE: Final[TokenType]   # which category of token this is (e.g. PLUS)
    LEXEME: Final[str]       # the exact source text, e.g. "!=" or "foo"
    LITERAL: Final[object]   # runtime value for literals (str/float), else None
    LINE: Final[int]         # source line the lexeme appeared on, for errors

    def __init__(self: Self, type:TokenType, lexeme: str, literal: object, line: int) -> None:
        """Store the token's category, source text, literal value, and line."""
        self.TYPE = type
        self.LEXEME = lexeme
        self.LITERAL = literal
        self.LINE = line

    def __repr__(self) -> str:
        """Human-readable form used when printing tokens (debug output)."""
        return f"{self.TYPE} {self.LEXEME} {self.LITERAL}"
