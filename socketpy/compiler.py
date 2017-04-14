import os
from subprocess import call


class Compiler:

    def __init__(self):
        self.working_directory = os.getcwd()

    def compile_library(self):
        sockets = os.path.join(self.working_directory, "sockets")
        os.chdir(sockets)
        call(["gcc", "-c", "-fpic", "paquetes.c"])
        call(["gcc", "-shared", "-o", "libsockets.so", "paquetes.o"])

