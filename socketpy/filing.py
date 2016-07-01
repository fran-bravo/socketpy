import os
from shutil import rmtree, copytree
from .analyzer import Analyzer
from socketpy.excpetions import FileError, ArgumentError


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
        self.defined_struct = ""
        self.number_struct = 0
        self.package = ""
        self.lines = ""
        self.includes = ""
        self.update = False
        self.analyzer = Analyzer()

    # Public Interface #

    def write_model(self, *args):
        parameters = args[0]
        struct = parameters.pop(0)
        self._read_model_file(struct)
        self._process_input(parameters, struct)
        # self.examine_context()
        self._write_model()
        self._read_package_file(struct)
        self._write_package()
        return struct

    def examine_context(self):
        print("Struct: ", self.struct)
        print("Defined Struct: ", self.defined_struct)
        print("Package: ", self.package)
        return

    def delete_sockets(self):
        try:
            print("Borrando sockets")
            rmtree(os.path.join(self.working_directory, "sockets"))
            print("Sockets borrados")
        except OSError as e:
            raise FileError(e)

    # Private Methods #

    def copy_templates(self):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headers")
        path = os.path.join(self.working_directory, "sockets")
        # print("Base: ", base_path, "Path: ", path)
        if not os.path.exists(path):
            copytree(base_path, path)
            print("\tCopiados templates de sockets")
        return path

    # File Reading #

    def _read_model_file(self, struct):
        print("\tLeyendo archivo de modelos")
        path = os.path.join(os.path.join(self.working_directory, "sockets"), "modelos.h")
        fd = FileLineWrapper(open(path, "r"))
        self._inspect_old_struct(struct, fd)
        return

    def _read_package_file(self, struct):
        print("\tLeyendo archivos de paquetes")
        path = os.path.join(os.path.join(self.working_directory, "sockets"), "paquetes.c")
        fd = FileLineWrapper(open(path, "r"))
        self._inspect_old_package(struct, fd)
        return

    # Inner Processing #

    def _inspect_old_struct(self, struct, fd):  # Determina que lineas incluir de modelos.h
        inside_struct_body = False
        for line in fd.f:
            self._count_defined_structs(line)
            self._found_define_struct(line, struct)
            if line != "\n":  # Ignoro lineas en blanco
                if inside_struct_body:  # Ignoro de la struct ya definida
                    if struct in line:  # Delimito el final del typedef
                        inside_struct_body = not inside_struct_body
                else:
                    if struct in line:  # Encuentro struct ya definida
                        inside_struct_body = not inside_struct_body
                    else:  # Lineas comunes
                        self.lines += line
        return

    def _inspect_old_package(self, struct, fd):  # Determina que lineas incluir de paquetes.c
        inside_switch_body = False
        for line in fd.f:
            if line != "\n":  # Ignoro lineas en blanco
                if inside_switch_body:  # Ignoro lineas del switch ya definido
                    if "break;" in line:  # Delimito el final del switch
                        inside_switch_body = not inside_switch_body
                else:
                    if struct.upper() in line:  # Encuentro switch ya definido
                        self.update = True
                        inside_switch_body = not inside_switch_body
                    else:  # Lineas comunes
                        self.lines += line
        return

    def _found_define_struct(self, line, struct):
        if struct.upper() in line:
            self.update = True
            self.number_struct -= 1
        return

    def _count_defined_structs(self, line):
        if "#define D" in line:
            self.number_struct += 1
        return

    def _prepare_model_lines(self):
        header, footer = self.lines.split("#endif")
        self.lines = header + self.includes + self.defined_struct + self.struct + "#endif\n" + footer
        return

    def _prepare_package_lines(self):
        header, middle, footer = self.lines.split("} //Fin del switch\n")
        self.lines = header + self.package + "\t} //Fin del switch\n" + middle + self.package + "\t} //Fin del switch\n" + footer
        return

    def _process_input(self, parameters, struct):
        print("\tProcesando input")
        self._process_arguments(parameters)
        self._process_struct(struct)
        self._define_struct(struct)
        self._process_package(struct)
        return

    def _process_arguments(self, parameters):
        for par in parameters:
            tipo, selector = self._split_selector(par)
            if self.analyzer.analyze_type(tipo):
                self.attributes[selector] = tipo
                if self.analyzer.source_type:
                    self._add_include()
            else:
                raise TypeError('El tipo de dato: ' + tipo + ' no es un tipo valido')

    def _add_include(self):
        if (self.analyzer.source_file not in self.lines) and (self.analyzer.source_file != "modelos.h"):
            self.includes += "#include <" + self.analyzer.source_file + ">\n"

    def _define_struct(self, struct):
        if not self.update:
            self.defined_struct = "\n#define D_" + struct.upper() + " " + str(self.number_struct) + "\n"
        return

    def _process_struct(self, struct):
        self.struct = "\ntypedef struct " + struct + "{\n"
        for key in self.attributes.keys():
            attr = "\t" + str(self.attributes[key]) + " " + key + ";\n"
            self.struct += attr
        self.struct += "} __attribute__ ((__packed__)) " + struct + ";\n\n"
        return

    def _process_package(self, struct):
        self.package = "\tcase D_" + struct.upper() + \
                       ":\n\t\t\t//TODO: definir funcion\n\t\t\tbreak;\n\t"
        return

    # File Writing

    def _write_model(self):
        print("\tEscribiendo modelos")
        self._prepare_model_lines()
        path = os.path.join(os.path.join(self.working_directory, "sockets"), "modelos.h")
        fd = FileLineWrapper(open(path, "w"))
        fd.f.writelines(self.lines)
        self.update = False
        self.lines = ""
        return

    def _write_package(self):
        print("\tEscribiendo paquetes")
        self._prepare_package_lines()
        path = os.path.join(os.path.join(self.working_directory, "sockets"), "paquetes.c")
        fd = FileLineWrapper(open(path, "w"))
        fd.f.writelines(self.lines)
        return

    # Auxiliary

    def _split_selector(self, string):
        if len(list(string.split(":"))) == 2:
            tipo, selector = string.split(":")
        else:
            raise ArgumentError("El formato de los argumentos ingresados es incorrecto. El formato es tipo:nombre")
        return tipo, selector
