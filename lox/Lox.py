from typing import Self

class Lox():
    had_error: bool = False

    @classmethod
    def run_file(cls: type[Self], path: str) -> None: 
        """Reads file from path and runs it."""
        with open(path, "r", encoding="utf-8") as f:
            bytes = f.read()
        cls.run(bytes)
        if (cls.had_error):
            exit(65)

    @classmethod
    def run_prompt(cls: type[Self]) -> None:
        while(True):
            try:
                line = input("> ")
            except EOFError:
                break
            cls.run(line)
            cls.had_error = False

    @classmethod
    def run(cls: type[Self], source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    @classmethod
    def error(cls: type[Self], line: int, message: str) -> None:
        cls.report(line, "", message)
        
    @classmethod
    def report(cls: type[Self], line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        cls.had_error = True
    