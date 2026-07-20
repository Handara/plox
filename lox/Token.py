from typing import Final
from typing import Self

import TokenType

class Token:
    TYPE: Final[TokenType]
    LEXEME: Final[str]
    LITERAL: Final[object]
    LINE: Final[int]

    def __init__(self: Self, type:TokenType, lexeme: str, literal: object, line: int) -> None:
        self.TYPE = type
        self.LEXEME = lexeme
        self.LITERAL = literal
        self.LINE = line

    def __repr__(self) -> str:
        return f"{self.TYPE} {self.LEXEME} {self.LITERAL}"
    