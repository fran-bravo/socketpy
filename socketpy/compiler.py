import os
from subprocess import call


class Compiler:

    def __init__(self):
        self.working_directory = os.getcwd()
        self.sockets = os.path.join(self.working_directory, "sockets")

    def compile_library(self):
        """
        Goes into sockets folder, builds objects and copies library files into global users includes
        
        :return: None 
        """

        os.chdir(self.sockets)
        self._build_objects()
        headers = self._find_headers()
        for h in headers:
            call(["cp", "-u", h, "/usr/include"])

    def _find_headers(self):
        """
        Searches all header files in sockets folder
        
        :return: list of header files
        """

        headers = []
        directories = list(os.walk(self.sockets))
        for direc in directories:
            root, subdirs, files = direc
            for fd in files:
                if fd.endswith('.h'):
                    headers.append(fd)
        return headers

    @staticmethod
    def _build_objects():
        """
        Executes basic build commands
        
        :return: None 
        """
        
        call(["gcc", "-c", "-fpic", "paquetes.c"])
        call(["gcc", "-shared", "-o", "libsockets.so", "paquetes.o"])
        call(["cp", "-u", "libsockets.so", "/usr/lib"])
