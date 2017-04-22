import os
from subprocess import call


class Compiler:

    def __init__(self):
        self.working_directory = os.getcwd()
        self.sockets = os.path.join(self.working_directory, "sockets")
        self.includes = os.path.abspath("/usr/include")
        self.libs = os.path.abspath("/usr/lib")

    def compile_library(self):
        """
        Goes into sockets folder, builds objects and copies library files into global users includes
        
        :return: None 
        """

        self._build_objects()
        headers = self._find_headers()
        for h in headers:
            call(["sudo", "cp", "-u", h, "/usr/include/"])
        os.chdir(self.working_directory)

    def decompile_library(self):
        """
        Deletes compiled files from system and removes built objects in sockets
        
        :return: 
        """

        self._delete_includes()
        self._delete_lib()
        self._unbuild_objects()
        os.chdir(self.working_directory)

    def _delete_includes(self):
        """
        Removes headers in includes
        
        :return: 
        """

        os.chdir(self.includes)
        headers = self._find_headers()
        for h in headers:
            call(["sudo", "rm", h])

    def _delete_lib(self):
        """
        Removes the libsockets file from /lib
        
        :return: 
        """

        os.chdir(self.libs)
        call(["sudo", "rm", "libsockets.so"])

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

    def _build_objects(self):
        """
        Executes basic build commands
        
        :return: None 
        """

        os.chdir(self.sockets)
        call(["gcc", "-c", "-fpic", "paquetes.c"])
        call(["gcc", "-shared", "-o", "libsockets.so", "paquetes.o"])
        call(["sudo", "cp", "-u", "libsockets.so", "/usr/lib"])

    def _unbuild_objects(self):
        """
        Deletes objects created by compile in /sockets

        :return: None 
        """

        os.chdir(self.sockets)
        call(["rm", "paquetes.o"])
        call(["rm", "libsockets.so"])
