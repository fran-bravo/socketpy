PACK_BODY = "{\n\t//TODO: definir funcion\n"


class Formatter(object):

    def prepare_lines(self, lines):
        """
        Defines the base prepare_lines method
        
        :param lines: 
        :return: 
        """
        pass

    def inspect(self, struct, fd, filing):
        """
        Defines the base inspect method
        
        :param struct: 
        :param fd: 
        :param filing: 
        :return: 
        """
        pass


class ModelFormatter(Formatter):

    def __init__(self, includes=None, defined_struct=None, struct=None):
        self.file = "modelos.h"
        self.includes = includes
        self.defined_struct = defined_struct
        self.struct = struct

    def prepare_lines(self, lines):
        """
        Splits the lines and adds the lines associated with the new struct
        
        :param lines: str with the lines of modelos.h file 
        :return: lines
        """

        header, footer = lines.split("#endif")
        lines = header + self.includes + self.defined_struct + self.struct + "#endif\n" + footer
        return lines

    def inspect(self, struct, fd, filing):
        """
        Inspects the file and filters its lines accordingly
        
        :param struct: str with the name of the new struct 
        :param fd: FileLineWrapper of modelos.h
        :param filing: Filer that is handling the inspection
        :return: None
        """

        inside_struct_body = False
        for line in fd.f:
            filing.count_defined_structs(line)
            filing.found_define_struct(line, struct)
            if line != "\n":  # Ignoro lineas en blanco
                if inside_struct_body:  # Ignoro de la struct ya definida
                    if struct in line:  # Delimito el final del typedef
                        inside_struct_body = not inside_struct_body
                else:
                    if struct in line:  # Encuentro struct ya definida
                        inside_struct_body = not inside_struct_body
                    else:  # Lineas comunes
                        filing.lines += line


class PackCFormatter(Formatter):

    def __init__(self, struct=None, package=None, package_functions=None, unpackage_functions=None):
        self.file = "paquetes.c"
        self.struct = struct
        self.package = package
        self.package_functions = package_functions
        self.unpackage_functions = unpackage_functions

    def prepare_lines(self, lines):
        """
        Splits the lines and adds the lines associated with the new struct
        
        :param lines: str with the lines of paquetes.c file 
        :return: lines
        """
        header, middle, footer = lines.split("} //Fin del switch\n")
        lines = header + self.package + "\t} //Fin del switch\n" + middle + self.package + \
                                        "\t} //Fin del switch\n" + footer
        header, middle, footer = lines.split("// Auxiliar\n")
        lines = header + "// Auxiliar\n" + middle + self.package_functions + \
                         PACK_BODY + "\tt_stream * paquete = malloc(sizeof(t_stream));\n" + \
                         "\treturn paquete;\n}\n" + "// Auxiliar\n" + self.unpackage_functions + \
                         PACK_BODY + "\tint tamanoCodigo = sizeof(" + self.struct + ");\n" + \
                         "\t" + self.struct + "* estructuraDestino = malloc(tamanoCodigo);\n" + \
                         "\treturn estructuraDestino;\n}\n" + footer
        return lines

    def inspect(self, struct, fd, filing):
        """
        Inspects the file and filters its lines accordingly

        :param struct: str with the name of the new struct 
        :param fd: FileLineWrapper of paquetes.c
        :param filing: Filer that is handling the inspection
        :return: None
        """

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
                        filing.update = True
                        inside_switch_body = not inside_switch_body
                    elif struct.lower() in line:  # Encuentro funcion de la struct
                        inside_function = not inside_function
                    else:  # Lineas comunes
                        filing.lines += line


class PackHFormatter(Formatter):

    def __init__(self, package_functions=None, unpackage_functions=None):
        self.file = "paquetes.h"
        self.package_functions = package_functions
        self.unpackage_functions = unpackage_functions

    def prepare_lines(self, lines):
        """
        Splits the lines and adds the lines associated with the new struct

        :param lines: str with the lines of paquetes.h file 
        :return: lines
        """
        header, footer = lines.split("// Auxiliar\n")
        lines = header + "// Auxiliar\n" + self.package_functions + ";\n" + \
                              self.unpackage_functions + ";\n" + footer
        return lines

    def inspect(self, struct, fd, filing):
        """
        Inspects the file and filters its lines accordingly

        :param struct: str with the name of the new struct 
        :param fd: FileLineWrapper of paquetes.h
        :param filing: Filer that is handling the inspection
        :return: None
        """
        for line in fd.f:
            if line != "\n":  # Ignoro lineas en blanco
                if struct.lower() not in line:    # Lineas comunes
                    filing.lines += line
