from typing import Self

from .ErrorReporter import ErrorReporter
from .Scanner import Scanner

class Lox():

    @classmethod
    def run_file(cls: type[Self], path: str) -> None:
        """Reads file from path and runs it."""
        with open(path, "r", encoding="utf-8") as f:
            bytes = f.read()
        cls.run(bytes)
        if (ErrorReporter.had_error):
            exit(65)

    @classmethod
    def run_prompt(cls: type[Self]) -> None:
        while(True):
            try:
                line = input("> ")
            except EOFError:
                break
            cls.run(line)
            ErrorReporter.had_error = False

    @classmethod
    def run(cls: type[Self], source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)
