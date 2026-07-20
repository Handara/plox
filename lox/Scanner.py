from typing import Final, Self

from .ErrorReporter import ErrorReporter
from .Token import Token
from .TokenType import TokenType

class Scanner:

    def __init__(self: Self, source: str) -> None:
        self._source: Final[str] = source
        self._tokens: Final[list[Token]] = list()
        self._start: int = 0
        self._current: int = 0
        self._line = 1

    def scan_tokens(self) -> list[Token]:
        while(not self._is_at_end()):
            self._start = self._current
            self._scan_token()
        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _scan_token(self: Self) -> None:
        c: str = self._advance()
        match c:
            case '(':
                return self._add_token(TokenType.LEFT_PAREN)
            case ')':
                return self._add_token(TokenType.RIGHT_PAREN)
            case '{':
                return self._add_token(TokenType.LEFT_BRACE)
            case '}':
                return self._add_token(TokenType.RIGHT_BRACE)
            case ',':
                return self._add_token(TokenType.COMMA)
            case '.':
                return self._add_token(TokenType.DOT)
            case '-':
                return self._add_token(TokenType.MINUS)
            case '+':
                return self._add_token(TokenType.PLUS)
            case ';':
                return self._add_token(TokenType.SEMICOLON)
            case '*':
                return self._add_token(TokenType.STAR)
            case '!':
                return self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
            case '=':
                return self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
            case '<':
                return self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
            case '>':
                return self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
            case _:
                ErrorReporter.error(self._line, "Unexpected character.")
                return

    def _match(self:Self, expected: str) -> bool:
        if (self._is_at_end()): return False
        if (self._source[self._current] != expected): return False

        self._current += 1
        return True

    def _is_at_end(self: Self) -> bool:
        return self._current >= len(self._source)

    def _advance(self: Self) -> str:
        self._current += 1
        return self._source[self._current - 1]

    def _add_token(self: Self, type: TokenType, literal: object = None) -> None:
        text: str = self._source[self._start:self._current]
        self._tokens.append(Token(type, text, literal, self._line))
