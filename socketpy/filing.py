import os
from shutil import rmtree, copytree
from .analyzer import Analyzer
from socketpy.exceptions import FileError, ArgumentError

PACK_BODY = "{\n\t//TODO: definir funcion\n}\n"


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
        self.package_functions = ""
        self.unpackage_functions = ""
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
        self._read_package_c_file(struct)
        self._write_package_c()
        self._read_package_h_file(struct)
        self._write_package_h()
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

    def _read_package_c_file(self, struct):
        print("\tLeyendo archivos de paquetes")
        path = os.path.join(os.path.join(self.working_directory, "sockets"), "paquetes.c")
        fd = FileLineWrapper(open(path, "r"))
        self._inspect_old_package_c(struct, fd)
        return

    def _read_package_h_file(self, struct):
        path = os.path.join(os.path.join(self.working_directory, "sockets"), "paquetes.h")
        fd = FileLineWrapper(open(path, "r"))
        self._inspect_old_package_h(struct, fd)
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

    def _inspect_old_package_c(self, struct, fd):  # Determina que lineas incluir de paquetes.c
        inside_switch_body = False
        inside_function = False
        for line in fd.f:
            if line != "\n":  # Ignoro lineas en blanco
                if inside_switch_body:  # Ignoro lineas del switch ya definido
                    if "break;" in line:  # Delimito el final del switch
                        inside_switch_body = not inside_switch_body
                elif inside_function:
                    if "}\n" == line:
                        inside_function = not inside_function
                else:
                    if struct.upper() in line:  # Encuentro switch ya definido
                        self.update = True
                        inside_switch_body = not inside_switch_body
                    elif struct.lower() in line:    # Encuentro funcion de la struct
                        inside_function = not inside_function
                    else:  # Lineas comunes
                        self.lines += line
        return

    def _inspect_old_package_h(self, struct, fd):
        for line in fd.f:
            if line != "\n":  # Ignoro lineas en blanco
                if struct.lower() not in line:    # Lineas comunes
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

    def _prepare_package_c_lines(self):
        header, middle, footer = self.lines.split("} //Fin del switch\n")
        self.lines = header + self.package + "\t} //Fin del switch\n" + middle + self.package + \
                                             "\t} //Fin del switch\n" + footer
        header, middle, footer = self.lines.split("// Auxiliar\n")
        self.lines = header + "// Auxiliar\n" + middle + self.package_functions + PACK_BODY + \
                              "// Auxiliar\n" + self.unpackage_functions + PACK_BODY + footer
        return

    def _prepare_package_h_lines(self):
        header, footer = self.lines.split("// Auxiliar\n")
        self.lines = header + "// Auxiliar\n" + self.package_functions + ";\n" + \
                              self.unpackage_functions + ";\n" + footer
        return

    def _process_input(self, parameters, struct):
        print("\tProcesando input")
        self._process_arguments(parameters)
        self._process_struct(struct)
        self._define_struct(struct)
        self._process_package(struct)
        self._process_package_functions(struct)
        return

    def _process_arguments(self, parameters):
        for par in parameters:
            selector, tipo = self._split_selector(par)
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

    def _process_package_functions(self, struct):
        print("Procesando funciones")
        self.package_functions = "t_stream* package_" + struct + "(" + struct + "* original_struct, " + \
                                 "uint8_t struct_type)"

        self.unpackage_functions = struct + "* unpackage_" + struct + "(char* data, uint16_t length)"

    # File Writing

    def _write_model(self):
        print("\tEscribiendo modelos")
        self._prepare_model_lines()
        self._write_file("modelos.h")
        self.update = False
        self.lines = ""
        return

    def _write_package_c(self):
        print("\tEscribiendo paquetes")
        self._prepare_package_c_lines()
        self._write_file("paquetes.c")
        self.update = False
        self.lines = ""
        return

    def _write_package_h(self):
        self._prepare_package_h_lines()
        self._write_file("paquetes.h")
        self.update = False
        self.lines = ""
        return

    # Auxiliary

    def _write_file(self, file):
        path = os.path.join(os.path.join(self.working_directory, "sockets"), file)
        fd = FileLineWrapper(open(path, "w"))
        fd.f.writelines(self.lines)
        fd.f.close()

    def _split_selector(self, string):
        if len(list(string.split(":"))) == 2:
            tipo, selector = string.split(":")
        else:
            raise ArgumentError("El formato de los argumentos ingresados es incorrecto. El formato es tipo:nombre")
        return tipo, selector
