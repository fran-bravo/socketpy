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

    def copy_models(self):
        base_path = os.path.dirname(os.path.abspath(__file__)) + "\headers\modelos.h"
        path = self.working_directory + "\modelos.h"
        if not os.path.exists(path):
            copy(base_path, path)
        return path

    def write_model(self, *args):
        parameters = args[0]
        struct = parameters.pop(0)
        self._process_arguments(parameters)
        self._process_struct(struct)
        self._read_file()
        self._write_file()

    def _find_line(self):
        path = self.working_directory + "\modelos.h"
        fd = FileLineWrapper(open(path, "r"))
        line = fd.readline()
        while line != "//Delimiter\n":
            line = fd.readline()
        self.line = fd.line + 1

    def _read_file(self):
        path = self.working_directory + "\modelos.h"
        fd = FileLineWrapper(open(path, "r"))
        for line in fd.f:
            self.lines += line

    def _prepare_lines(self):
        header, footer = self.lines.split("//Delimiter:\n")
        self.lines = header + self.struct + "//Delimiter:\n" + footer

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
        self.struct = "typedef struct " + struct + "{\n"
        for key in self.attributes.keys():
            attr = "\t" + key + " " + str(self.attributes[key]) + ";\n"
            self.struct += attr
        self.struct += "} __attribute__ ((__packed__)) " + struct + ";\n\n"

    def _split_selector(self, string):
        tipo, selector = string.split(":")
        return tipo, selector