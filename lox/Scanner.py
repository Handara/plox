"""The lexical scanner (a.k.a. lexer).

Turns a flat string of Lox source code into a flat list of Tokens.
This is the first stage of the interpreter: it walks the source one
character at a time and groups characters into the smallest meaningful
chunks (lexemes) such as `(`, `!=`, `123`, `"hi"`, or `while`.
"""

from typing import Final, Self

from .ErrorReporter import ErrorReporter
from .Token import Token
from .TokenType import TokenType

class Scanner:
    """Scans a single Lox source string into a list of tokens.

    The scanner keeps a small cursor into `_source` and repeatedly carves
    out one lexeme at a time until it reaches the end of the input.
    """

    # Reserved words: identifiers that spell one of these are NOT variable
    # names but language keywords. Looked up in `_identifier` after reading
    # a run of letters. Shared by every Scanner, so it lives on the class.
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
        """Store the source and initialise the scanning cursor."""
        self._source: Final[str] = source        # the raw text being scanned
        self._tokens: Final[list[Token]] = list() # tokens produced so far
        self._start: int = 0    # index of the first char of the current lexeme
        self._current: int = 0  # index of the char currently being looked at
        self._line: int = 1     # 1-based line number, for error messages

    def scan_tokens(self) -> list[Token]:
        """Scan the whole source and return the full token list.

        Loops until the source is exhausted, carving out one lexeme per
        iteration, then appends a final end-of-file marker token.
        """
        while(not self._is_at_end()):
            # We are at the beginning of the next lexeme.
            self._start = self._current
            self._scan_token()
        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _scan_token(self: Self) -> None:
        """Read one lexeme starting at the cursor and add its token.

        Consumes at least one character (via `_advance`) and dispatches on
        it. Single-char lexemes add a token directly; two-char operators
        peek ahead with `_match`; whitespace is skipped; and anything more
        complex (comments, strings, numbers, identifiers) delegates to a
        helper.
        """
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
            # For these, a trailing '=' turns a one-char operator into a
            # two-char one (e.g. '!' vs '!='). `_match` consumes the '='.
            case '!':
                return self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
            case '=':
                return self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
            case '<':
                return self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
            case '>':
                return self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
            case '/':
                # '//' begins a line comment: swallow chars until newline.
                # A single '/' is the division operator.
                if self._match('/'):
                    while(self._peek() != '\n' and not self._is_at_end()): self._advance()

                # '/*' begins a block comment: swallow chars until matching '*/'
                elif self._match('*'):
                    # if next character is * and the character after is * and we are not at the end of file 
                    while(not (self._peek() == '*' and self._peek_next() == '/') and not self._is_at_end()):
                        if(self._peek() == '\n'): self._line += 1
                        self._advance()
                    if ((self._peek() == '*' and self._peek_next() == '/')):
                        self._advance()
                        self._advance()
                    else:
                        ErrorReporter.report(self._line, "Unterminated block comment.")
                else:
                    return self._add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                # Insignificant whitespace: ignore and move on.
                return
            case '\n':
                # Newlines are whitespace too, but bump the line counter.
                self._line += 1
                return
            case '"':
                return self._string()
            case _:
                # Numbers and identifiers have too many first-chars to list
                # as match cases, so classify the character here instead.
                if self._is_digit(c): self._number()
                elif self._is_alpha(c): self._identifier()
                else: ErrorReporter.error(self._line, "Unexpected character.")
                return

    def _identifier(self: Self) -> None:
        """Consume an identifier or keyword lexeme and add its token.

        Called after the first letter has been read. Keeps consuming
        letters/digits, then checks whether the resulting word is a
        reserved keyword; if not, it is a user identifier.
        """
        while self._is_alpha_numeric(self._peek()): self._advance()

        text: str = self._source[self._start: self._current]
        type: TokenType = self.keywords.get(text)
        if(type == None): type = TokenType.IDENTIFIER
        self._add_token(type)


    def _string(self: Self) -> None:
        """Consume a string literal and add its token.

        Called after the opening `"` has been read. Consumes characters
        (allowing multi-line strings) until the closing `"`; reports an
        error if the source ends first. The token's literal value is the
        text with the surrounding quotes stripped off.
        """
        while (self._peek() != '"' and not self._is_at_end()):
            if (self._peek()!= '\n'): self._line+=1
            self._advance()
        if self._is_at_end():
            ErrorReporter.error(self._line, "Unterminated string")
            return

        # Consume the closing '"'.
        self._advance()

        # Trim the surrounding quotes for the literal value.
        value :str = self._source[self._start + 1, self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _match(self: Self, expected: str) -> bool:
        """Conditional advance: consume the next char only if it matches.

        Returns True (and moves the cursor forward) when the current char
        equals `expected`; otherwise leaves the cursor put and returns
        False. This is how two-character operators are recognised.
        """
        if self._is_at_end(): return False
        if self._source[self._current] != expected: return False

        self._current += 1
        return True

    def _peek(self: Self) -> str:
        """Return the current char without consuming it (1-char lookahead).

        Returns the null char '\\0' at end of input so callers don't have
        to special-case the boundary.
        """
        if self._is_at_end(): return '\0'
        return self._source[self._current]

    def _peek_next(self: Self) -> str:
        """Return the char after the current one (2-char lookahead).

        Used to decide whether a '.' inside a number is a decimal point
        (needs a digit after it) or something else.
        """
        if self._current +1 >= len(self._source): return '\0'
        return self._source[self._current + 1]

    def _is_alpha(self:Self, c: str) -> bool:
        """True if `c` may start/continue an identifier (a-z, A-Z, or _)."""
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')

    def _is_alpha_numeric(self: Self, c: str):
        """True if `c` is a letter, underscore, or digit."""
        return self._is_alpha(c) or self._is_digit(c)

    def _is_digit(self:Self, c: str) -> bool:
        """True if `c` is an ASCII digit 0-9."""
        return c >= '0' and c <= '9'

    def _number(self: Self) -> None:
        """Consume a numeric literal and add its token.

        Called after the first digit has been read. Consumes the integer
        part, then an optional fractional part (a '.' immediately followed
        by more digits). All Lox numbers are stored as Python floats.
        """
        while (self._is_digit(self._peek())): self._advance()

        # Only treat '.' as a decimal point if a digit follows it, so that
        # e.g. `123.method` isn't misread as the number `123.`.
        if (self._peek() == '.' and self._is_digit(self._peek_next())):

            self._advance()

            while self._is_digit(self._peek()): self._advance()

        self._add_token(TokenType.NUMBER, float(self._source[self._start, self._current]))

    def _is_at_end(self: Self) -> bool:
        """True once the cursor has consumed every character of the source."""
        return self._current >= len(self._source)

    def _advance(self: Self) -> str:
        """Consume the current char and return it (unconditional advance)."""
        self._current += 1
        return self._source[self._current - 1]

    def _add_token(self: Self, type: TokenType, literal: object = None) -> None:
        """Create a token for the current lexeme and append it.

        The lexeme text is the slice of source from `_start` to `_current`.
        `literal` is the runtime value for literals (a str or float) and
        None for everything else.
        """
        text: str = self._source[self._start:self._current]
        self._tokens.append(Token(type, text, literal, self._line))
