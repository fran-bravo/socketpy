#!/usr/bin/python3
import sys
import os

path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

import socketpy


def main(args=None):
    socketpy.main()


if __name__ == '__main__':
    sys.exit(main())
