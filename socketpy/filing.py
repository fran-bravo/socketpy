import os
from shutil import rmtree, copytree
from socketpy.analyzer import Analyzer
from socketpy.exceptions import FileError, ArgumentError
from socketpy.formatter import ModelFormatter, PackHFormatter, PackCFormatter


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
        """
        Writes socket files accordingly for handling the new struct to be defined with args
        
        :param args: list of arguments obtained by the parser 
        :return: str with the struct name
        """

        parameters = args[0]
        struct = parameters.pop(0)
        self._read_file(struct, ModelFormatter())
        self._process_input(parameters, struct)
        # self.examine_context()
        self._write_with_format(self._generate_model_formatter())
        self._read_file(struct, PackCFormatter())
        self._write_with_format(self._generate_pack_c_formatter())
        self._read_file(struct, PackHFormatter())
        self._write_with_format(self._generate_pack_h_formatter())
        return struct

    def examine_context(self):
        """
        Examines the context of the filer at any given time
        
        :return: None 
        """

        print("Struct: ", self.struct)
        print("Defined Struct: ", self.defined_struct)
        print("Package: ", self.package)
        return

    def delete_sockets(self):
        """
        Deletes the sockets folder and its files
        
        :return: None or an error 
        """

        try:
            print("Borrando sockets")
            rmtree(os.path.join(self.working_directory, "sockets"))
            print("Sockets borrados")
        except OSError as e:
            raise FileError(e)

    def copy_templates(self):
        """
        Copies the base tree of the templates used by socketpy in the directory where it is called
        
        :return: str with the path to new sockets folder 
        """

        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headers")
        path = os.path.join(self.working_directory, "sockets")
        # print("Base: ", base_path, "Path: ", path)
        if not os.path.exists(path):
            copytree(base_path, path)
            print("\tCopiados templates de sockets")
        return path

    # Private Methods #

    # File Reading #

    def _read_file(self, struct, formatter):
        """
        Reads a specific file and filters its lines based on the struct
        
        :param struct: str with the name of the struct to be added 
        :param formatter: Formatter which specifies the file and the way to inspect it
        :return: None
        """

        print("\tLeyendo archivo {}".format(formatter.file))
        path = os.path.join(os.path.join(self.working_directory, "sockets"), formatter.file)
        fd = FileLineWrapper(open(path, "r"))
        formatter.inspect(struct, fd, self)
        return

    # Inner Processing #

    def found_define_struct(self, line, struct):
        """
        Validates if the line is a DEFINE of the struct. If so, turns on update flag and decreases number_struct counter
        
        :param line: str of the line analyzed 
        :param struct: str with the name of the struct
        :return: None
        """

        if struct.upper() in line:
            self.update = True
            self.number_struct -= 1
        return

    def count_defined_structs(self, line):
        """
        Validates if the line is a DEFINE expresion. If so, increase number_struct counter
        
        :param line: str of the line analyzed 
        :return: None
        """

        if "#define D" in line:
            self.number_struct += 1
        return

    def _process_input(self, parameters, struct):
        """
        Processes all the parameters and the struct and defines lines to be added in the files
        
        :param parameters: list of parameters which define attributes of the struct 
        :param struct: str with the name of the struct
        :return: None
        """

        print("\tProcesando input")
        self._process_arguments(parameters)
        self._process_struct(struct)
        self._define_struct(struct)
        self._process_package(struct)
        self._process_package_functions(struct)
        return

    def _process_arguments(self, parameters):
        """
        Iterates the parameters and adds the couple selector-tipo to attributes dict
        
        :param parameters: list of parameters of the struct
        :return: None or error
        """

        for par in parameters:
            selector, tipo = self._split_selector(par)
            if self.analyzer.analyze_type(tipo):
                self.attributes[selector] = tipo
                if self.analyzer.source_type:
                    self._add_include()
            else:
                raise TypeError('El tipo de dato: ' + tipo + ' no es un tipo valido')

    def _add_include(self):
        """
        If the source file of the struct added is not included it adds it to the file
        
        :return: None 
        """
        
        print("Source {}".format(self.analyzer.source_file))
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

    def _write_with_format(self, formatter):
        print("\tEscribiendo {}".format(formatter.file))
        self.lines = formatter.prepare_lines(self.lines)
        self._write_file(formatter.file)
        self.update = False
        self.lines = ""
        return

    # Generate Formatters

    def _generate_model_formatter(self):
        return ModelFormatter(self.includes, self.defined_struct, self.struct)

    def _generate_pack_c_formatter(self):
        return PackCFormatter(self.package, self.package_functions, self.unpackage_functions)

    def _generate_pack_h_formatter(self):
        return PackHFormatter(self.package_functions, self.unpackage_functions)

    # Auxiliary

    def _write_file(self, file):
        path = os.path.join(os.path.join(self.working_directory, "sockets"), file)
        fd = FileLineWrapper(open(path, "w"))
        fd.f.writelines(self.lines)
        fd.f.close()

    @staticmethod
    def _split_selector(string):
        if len(list(string.split(":"))) == 2:
            tipo, selector = string.split(":")
        else:
            raise ArgumentError("El formato de los argumentos ingresados es incorrecto. El formato es tipo:nombre")
        return tipo, selector
