from typing import Final, Self

from .ErrorReporter import ErrorReporter
from .Token import Token
from .TokenType import TokenType

class Scanner:
    
    
    keywords: Final[dict[str, TokenType]] = {
        "and"    : TokenType.AND,
        "class"  : TokenType.CLASS,
        "else"   : TokenType.ELSE,
        "false"  : TokenType.FALSE,
        "for"    : TokenType.FOR,
        "fun"    : TokenType.FUN, 
        "if"     : TokenType.IF,
        "nil"    : TokenType.NIL,
        "or"     : TokenType.OR,
        "print"  : TokenType.PRINT,
        "return" : TokenType.RETURN,
        "super"  : TokenType.SUPER,
        "this"   : TokenType.THIS,
        "true"   : TokenType.TRUE,
        "var"    : TokenType.VAR,
        "while"  : TokenType.WHILE,
    } 
    def __init__(self: Self, source: str) -> None:
        self._source: Final[str] = source
        self._tokens: Final[list[Token]] = list()
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1

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
            case '/':
                if self._match('/'): 
                    while(self._peek() != '\n' and not self._is_at_end()): self._advance()
                else:
                    return self._add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                return
            case '\n':
                self._line += 1
                return
            case '"':
                return self._string()
            case _:
                if self._is_digit(c): self._number()
                elif self._is_alpha(c): self._identifier()
                else: ErrorReporter.error(self._line, "Unexpected character.")
                return

    def _identifier(self: Self) -> None:
        while self._is_alpha_numeric(self._peek()): self._advance()

        text: str = self._source[self._start, self._current]
        type: TokenType = self.keywords.get(text)
        if(type == None): type = TokenType.IDENTIFIER
        self._add_token(type)


    def _string(self: Self) -> None:
        while (self._peek() != '"' and self._is_at_end()):
            if (self._peek()!= '\n'): self._line+=1
            self._advance()
        if self._is_at_end():
            ErrorReporter.error(self._line, "Unterminated string")
            return
        
        self._advance()

        value :str = self._source[self._start + 1, self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _match(self: Self, expected: str) -> bool:
        if self._is_at_end(): return False
        if self._source[self._current] != expected: return False

        self._current += 1
        return True

    def _peek(self: Self) -> str:
        if self._is_at_end(): return '\0'
        return self._source[self._current] 

    def _peek_next(self: Self) -> str:
        if self._current +1 >= len(self._source): return '\0'
        return self._source[self._current + 1]

    def _is_alpha(c: str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')

    def _is_alpha_numeric(self: Self, c: str):
        return self._is_alpha or self._is_digit

    def _is_digit(c: str) -> bool:
        return c >= '0' and c <= '9'

    def _number(self: Self) -> None:
        while (self._is_digit(self._peek())): self._advance

        if (self._peek() == '.' and self._is_digit(self._peek_next())):

            self._advance()

            while self._is_digit(self._peek()): self._advance()

        self._add_token(TokenType.NUMBER, float(self._source[self._start, self._current]))

    def _is_at_end(self: Self) -> bool:
        return self._current >= len(self._source)

    def _advance(self: Self) -> str:
        self._current += 1
        return self._source[self._current - 1]

    def _add_token(self: Self, type: TokenType, literal: object = None) -> None:
        text: str = self._source[self._start:self._current]
        self._tokens.append(Token(type, text, literal, self._line))
