from typing import Self


class ErrorReporter:

    had_error: bool = False

    @classmethod
    def error(cls: type[Self], line: int, message: str) -> None:
        cls.report(line, "", message)

    @classmethod
    def report(cls: type[Self], line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        cls.had_error = True
