class Lox():
    
    @staticmethod
    def main(args):
        """Entry point for the plox interpreter"""
        if len(args) > 1 :
            print("Usage : jlox [script]")
            exit(64)
        elif (len(args) == 1):
            runFile(args[0])
        else:
            runPrompt()
    
    @staticmethod
    def runFile(path):
        """Reads file from path and runs it."""
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        run(source)

    @staticmethod
    def runPrompt():
        while(True):
            try :
                line = input("> ")
            except EOFError:
                break
            run(line)
        