import sys
import os
from .parser import Parser, ParseError


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


if __name__ == '__main__':
    sys.exit(main())
