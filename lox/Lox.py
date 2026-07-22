"""The top-level driver for the Lox interpreter.

Owns the two ways to run Lox code — from a file or from an interactive
prompt — and the shared `run` routine both funnel into. At this stage of
the book `run` only scans and prints tokens; parsing and evaluation get
added in later chapters.
"""

from typing import Self

from .ErrorReporter import ErrorReporter
from .Scanner import Scanner

class Lox():
    """Namespace of class methods that drive a Lox session."""

    @classmethod
    def run_file(cls: type[Self], path: str) -> None:
        """Read the file at `path` and run it once.

        If any error was reported while running, exit with status 65
        """
        with open(path, "r", encoding="utf-8") as f:
            bytes = f.read()
        cls.run(bytes)
        if (ErrorReporter.had_error):
            exit(65)

    @classmethod
    def run_prompt(cls: type[Self]) -> None:
        """Run an interactive REPL, one line of Lox per prompt.

        Reads lines until end-of-input (Ctrl-D raises EOFError). A bad
        line reports an error but must NOT kill the session, so the error
        flag is reset after every line.
        """
        while(True):
            try:
                line = input("> ")
            except EOFError:
                break
            cls.run(line)
            ErrorReporter.had_error = False

    @classmethod
    def run(cls: type[Self], source: str) -> None:
        """Scan `source` into tokens and (for now) print each one."""
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)
