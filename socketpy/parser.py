import os
import sys


def help():
    print("Comandos disponibles: help")


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = Parser()

    try:
        parser.parse(args)
    except ParseError as exception:
        sys.stderr.write("ERROR: %s" % exception)
        sys.stderr.write(os.linesep)
        sys.exit(1)

    return


class Parser:

    def __init__(self):
        self.commands = {'help': help()}

    def parse(self, *args):
        print("Argumentos: ", *args)
        command = args.pop(0)

        try:
            self.commands[command](*args)
        except:
            raise ParseError


class ParseError(Exception):
    pass
