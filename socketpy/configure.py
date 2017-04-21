import sqlite3, os, re, sys
from socketpy.filing import FileLineWrapper
from socketpy.db import Database
from socketpy.analyzer import Analyzer
from socketpy.templates import MODEL, PACKC, PACKH


class Configure:

    def __init__(self):
        self.working_directory = os.getcwd()
        self.headers = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headers")
        self.database = Database()
        self.analyzed_files = []

    # Public Interface #

    def initialize_directories(self):
        """
        Creates base directories for socketpy
        
        :return: None 
        """

        self._create_directory("database")
        self._create_directory("headers")
        print("\tGenerados directorios database y headers")

    def create_db(self):
        """
        Creates the database, its tables and loads basic types
        
        :return: None 
        """

        print("\tInicializando db")
        self.database.create_tables()
        self._load_basic_types()

    def close_connection(self):
        """
        Closes the connection to the database
        
        :return: None 
        """

        self.database.close_connection()

    def create_headers(self):
        """
        Creates the base templates to be copied by socketpy
        
        :return: None 
        """

        self._create_file("modelos.h", MODEL)
        self._create_file("paquetes.h", PACKH)
        self._create_file("paquetes.c", PACKC)
        print("\tGenerados templates de sources a utilizar")

    def gather_types(self):
        """
        Walks through the working directory and gets the types from '.c' or '.h' files
        
        :return: None 
        """

        directories = list(os.walk(self.working_directory))
        for direc in directories:
            root, subdirs, files = direc
            for fd in files:
                if fd.endswith(".c") or fd.endswith(".h"):
                    self._analyze_file(root, fd)
                    print("\tNo hay más tipos de datos en el archivo\n")

    # Private Methods #

    def _analyze_file(self, root, source):
        """
        Makes the abs path with root and source, opens the file and explores its lines looking for types
        
        :param root: str root directory
        :param source: str file
        :return: None
        """

        file = os.path.join(root, source)
        print("Procesando archivo: ", source)
        fd = FileLineWrapper(open(file))
        self._explore_lines(fd, source)

    # Lines processing #

    def _explore_lines(self, fd, source):
        """
        Explores the lines of a file and gathers possible types
        
        :param fd: FileDescriptor 
        :param source: str file name
        :return: None
        """

        struct_body = 0
        for line in fd.f:
            line = line.lstrip()
            if line.startswith("#include"):     # Linea #include
                self._inspect_include(line)
            elif line.startswith("typedef") and line.endswith(";\n"):     # Linea typedef simple
                self._get_type_from_typedef_sentence(line, source)
            elif line.startswith("typedef") and (line.endswith("{") or line.endswith("\n")):   # Linea typedef compuesta
                struct_body += 1
            elif line.endswith("{\n"):
                struct_body += 1
            elif line.startswith("}"):    # Fin typedef compuesta
                struct_body -= 1
                if struct_body == 0:
                    self._get_type_from_typedef_end_sentence(line, source)

    # Line Analyzing #

    def _get_type_from_typedef_end_sentence(self, line, source):
        """
        Gets the type from the end of a typedef block
        
        :param line: str of the line analyzed 
        :param source: str of the file name
        :return: None
        """

        tipo = re.sub('[;}\ \n]', '', line)
        if tipo.startswith("__"):
            tipo = tipo.split("))")[1]
        if tipo != "":
            self.database.insert_type(tipo, source)

    def _get_type_from_typedef_sentence(self, line, source):
        """
        Gets the type from a typedef expression without block
        
        :param line: str of the line analyzed 
        :param source: str of the file name
        :return: None
        """

        analyzer = Analyzer()
        # TODO: Separar en diferentes analizadores de linea (punteros a funciones, structs, etc)
        print("Linea typedef simple: ", line)   # typedef struct ptw32_cleanup_t ptw32_cleanup_t;
        if re.match(r'(typedef) ' + analyzer.all() + ' (\()', line):
            print("Es un puntero")
            self._get_function_ptr(line, source)
        elif re.match('typedef struct', line):
            print("Es un struct")
            self._get_struct(line, source)
        elif re.match('typedef', line):
            print("Es un tipo basico")
            self._get_basic_type(line, source)

    def _get_struct(self, line, source):
        """
        Gets type from a struct in the typedef expression
        
        :param line: str of the line analyzed 
        :param source: str of the file name
        :return: None
        """

        linea = line.split(" ")
        tipo = linea[-1]
        tipo = re.sub('[\(\n;]', '', tipo)
        self.database.insert_type(tipo, source)

    def _get_function_ptr(self, line, source):
        """
        Gets type from a function pointer
        
        :param line: str of the line analyzed 
        :param source: str of the file name
        :return: 
        """

        linea = line.split(" ")
        tipo = linea[2]
        tipo = tipo.split(")")[0]
        print("Tipo: ", tipo)
        tipo = re.sub('[\(\*\n;]', '', tipo)
        self.database.insert_type(tipo, source)

    def _get_basic_type(self, line, source):
        """
        Gets type from a basic typedef expression
        
        :param line: str of the line analyzed 
        :param source: str of the file name
        :return: None
        """

        linea = line.replace("\t", " ")
        linea = linea.split(" ")
        tipo = linea[-1]
        tipo = re.sub('[\(\n;]', '', tipo)
        print("Tipo: ", tipo)
        self.database.insert_type(tipo, source)

    def _inspect_include(self, line):
        """
        Inspects an include and tries to find it in the routes of the database to keep looking for types
        
        :param line: str of the line analyzed 
        :return: None
        """

        print("Explorando include ", line)
        if "<" in line:
            file = line.split("<")[-1]
            file = re.sub('[>\n]', '', file)
            #if "/" in file:
            #    file = file.split("/")[-1]
            print("Archivo {}".format(file))
        if "\"" in line:
            file = line.split("\"")[-2]
        for root in self.database.get_routes():
            for dir, subdirs, files in os.walk(root):
                if file in files and file not in self.analyzed_files:
                    self._analyze_file(dir, file)
                    print("\tNo hay más tipos de dato en el archivo")
                    self.analyzed_files.append(file)
                    break
                elif file in self.analyzed_files:
                    print("El archivo {} ya fue analizado".format(file))
                    break
                else:
                    print("\tEl archivo incluido no se encuentra en las rutas definidas\n", end='')

    # Db initialization #

    def _load_basic_types(self):
        """
        Inserts basic types into the database
        
        :return: None 
        """

        types = [("int", "builtin"),
                 ("float", "builtin"), ("double", "builtin"),
                 ("void", "builtin"), ("char", "builtin"),
                 ("int*", "builtin"),
                 ("float*", "builtin"), ("double*", "builtin"),
                 ("void*", "builtin"), ("char*", "builtin"),
                 ]
        self.database.insert_types(types)

    # Directories initialization #

    @staticmethod
    def _create_directory(directory):
        """
        Creates a directory if it doesn't exist
        
        :param directory: str of the directory to create 
        :return: None
        """

        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), directory))

    #   Templates Creation  #

    def _create_file(self, file, lines):
        """
        Creates a file and writes the lines received
        
        :param file: str file to create
        :param lines: str lines to write
        :return: None
        """

        fd = FileLineWrapper(open(os.path.join(self.headers, file), "w+"))
        fd.f.writelines(lines)
        fd.close()
