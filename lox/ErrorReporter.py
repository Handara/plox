"""Centralised error reporting.

Kept in its own module (rather than on `Lox`) so that the Scanner can report errors without importing
Lox, which would create a circular import.
"""

from typing import Self


class ErrorReporter:
    """Collects and prints user-facing syntax/runtime errors.

    State and behaviour are class-level, so callers use it like
    `ErrorReporter.error(...)` without creating an instance.
    """

    # Set to True the moment any error is reported. `Lox.run_file` reads
    # this to decide whether to exit with a non-zero status code.
    had_error: bool = False

    @classmethod
    def error(cls: type[Self], line: int, message: str) -> None:
        """Report an error occurring on a given source line."""
        cls.report(line, "", message)

    @classmethod
    def report(cls: type[Self], line: int, where: str, message: str) -> None:
        """Print a formatted error and mark that an error occurred.
        """
        print(f"[line {line}] Error {where}: {message}")
        cls.had_error = True
