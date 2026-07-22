"""The set of token categories the scanner can emit.

`TokenType` is an enum: every lexeme the scanner recognises is tagged
with exactly one of these members. Later stages (parser, interpreter)
switch on the member instead of re-inspecting the raw text.

The `auto()` calls just hand each member a distinct value automatically;
the actual numbers don't matter, only that they're unique.
"""

from enum import Enum, auto

class TokenType(Enum):
    """ Single-character tokens """

    LEFT_PAREN    = auto()
    RIGHT_PAREN   = auto()
    LEFT_BRACE    = auto()
    RIGHT_BRACE   = auto()
    COMMA         = auto()
    DOT           = auto()
    MINUS         = auto()
    PLUS          = auto()
    SEMICOLON     = auto()
    SLASH         = auto()
    STAR          = auto()

    """ One or two character tokens """

    BANG          = auto()
    BANG_EQUAL    = auto()
    EQUAL         = auto()
    EQUAL_EQUAL   = auto()
    GREATER       = auto()
    GREATER_EQUAL = auto()
    LESS          = auto()
    LESS_EQUAL    = auto()

    """ Literals """

    IDENTIFIER    = auto()  # a name: variable, function, etc.
    STRING        = auto()  # "..." literal
    NUMBER        = auto()  # numeric literal (always a float in Lox)

    """ Keywords """

    AND           = auto()
    CLASS         = auto()
    ELSE          = auto()
    FALSE         = auto()
    FUN           = auto()
    FOR           = auto()
    IF            = auto()
    NIL           = auto()
    OR            = auto()
    PRINT         = auto()
    RETURN        = auto()
    SUPER         = auto()
    THIS          = auto()
    TRUE          = auto()
    VAR           = auto()
    WHILE         = auto()

    EOF           = auto()  # end-of-file sentinel appended after the last lexeme
