import os
from shutil import copy


class FileLineWrapper(object):
    def __init__(self, f):
        self.f = f
        self.line = 0

    def close(self):
        return self.f.close()

    def readline(self):
        self.line += 1
        return self.f.readline()


class Filer:

    def __init__(self):
        self.working_directory = os.getcwd()
        self.attributes = {}
        self.struct = ""
        self.lines = ""

    # Public Interface #

    def copy_files(self, models=False, sockets=False):
        if models:
            self._copy_files("modelos.h")
        elif sockets:
            self._copy_files("sockets.h")

    def write_file(self, *args, models=False, sockets=False):
        if models:
            self._write_model(*args)
        elif sockets:
            self._write_socket(*args)

    # Private Methods #

    def _copy_files(self, file_name):
        base_path = os.path.dirname(os.path.abspath(__file__)) + "\headers\\" + file_name
        path = self.working_directory + "\\" + file_name
        if not os.path.exists(path):
            copy(base_path, path)
        return path

    def _write_model(self, *args):
        parameters = args[0]
        struct = parameters.pop(0)
        self._process_arguments(parameters)
        self._process_struct(struct)
        self._read_file(struct)
        self._write_file()

    def _write_socket(self, *args):
        parameters = args[0]
        struct = parameters.pop(0)
        # TODO: Diseñar lo que se desea escribir en el archivo
        # self._process_arguments(parameters)
        # self._process_struct(struct)
        # self._read_file(struct)
        # self._write_file()
        return

    def _find_line(self):
        path = self.working_directory + "\modelos.h"
        fd = FileLineWrapper(open(path, "r"))
        line = fd.readline()
        while line != "//Delimiter\n":
            line = fd.readline()
        self.line = fd.line + 1

    def _read_file(self, struct):
        path = self.working_directory + "\modelos.h"
        fd = FileLineWrapper(open(path, "r"))
        self._inspect_old_struct(struct, fd)

    def _inspect_old_struct(self, struct, fd):
        struct_body = False
        for line in fd.f:
            if not struct_body:
                if struct in line:
                    struct_body = not struct_body
                else:
                    if line != "\n":
                        self.lines += line
            else:
                if struct in line:
                    struct_body = not struct_body

    def _prepare_lines(self):
        header, footer = self.lines.split("#endif\n")
        self.lines = header + self.struct + "#endif\n" + footer

    def _write_file(self):
        self._prepare_lines()
        path = self.working_directory + "\modelos.h"
        fd = FileLineWrapper(open(path, "w"))
        fd.f.writelines(self.lines)

    def _process_arguments(self, parameters):
        for par in parameters:
            tipo, selector = self._split_selector(par)
            self.attributes[tipo] = selector

    def _process_struct(self, struct):
        self.struct = "\ntypedef struct " + struct + "{\n"
        for key in self.attributes.keys():
            attr = "\t" + key + " " + str(self.attributes[key]) + ";\n"
            self.struct += attr
        self.struct += "} __attribute__ ((__packed__)) " + struct + ";\n\n"

    def _split_selector(self, string):
        tipo, selector = string.split(":")
        return tipo, selector
