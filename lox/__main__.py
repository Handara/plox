"""Package entry point: run with `python -m lox [script]`.

`__main__.py` is the file Python executes when a package is run with the
`-m` flag, which is why the CLI argument handling lives here.
"""

import sys

from .Lox import Lox

def main():
    """Dispatch based on how many command-line arguments were given.

    No args  -> start the interactive REPL.
    One arg  -> treat it as a path and run that script.
    More     -> print usage and exit with status 64.
    """
    if len(args) > 1 :
        print("Usage : jlox [script]")
        exit(64)
    elif (len(args) == 1):
        Lox.run_file(args[0])
    else:
        Lox.run_prompt()

if __name__ == "__main__":
    main(sys.argv[1:])
