import sys

from .Lox import Lox

def main(args):
    """Entry point for the plox interpreter"""
    if len(args) > 1 :
        print("Usage : jlox [script]")
        exit(64)
    elif (len(args) == 1):
        Lox.run_file(args[0])
    else:
        Lox.run_prompt()

if __name__ == "__main__":
    main(sys.argv[1:])
