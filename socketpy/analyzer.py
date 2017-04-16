import re
from socketpy.db import Database


class Analyzer:
    c_built_ins = []
    c_types = []
    c_built_in_array_types = r'^(' + '|'.join(c_built_ins) + ')\[[0-9]*\]'
    c_array_types = []

    def __init__(self):
        self._get_types()
        self.source_type = False
        self.source_file = ""

    def analyze_type(self, tipo):
        """
        Checks if given type is valid according to database types and possible arrays or pointers
        
        :param tipo: str type to be analyzed 
        :return: bool
        """

        if not self.c_types:
            return self._validate_built_in(tipo)
        elif tipo in self.c_types or self._match_array(tipo, self.c_array_types):
            return self._validate_source(tipo)
        else:
            return self._validate_built_in(tipo)

    def all(self):
        """
        Formats all types for a regex evaluation
        
        :return: str to use in regex 
        """

        built = '|'.join(self.escaped(self.c_built_ins))
        types = '|'.join(self.escaped(self.c_types))
        built_arr = '|'.join(self.escaped(self.c_built_ins)) + '\[[0-9]*\]'
        types_arr = '|'.join(self.escaped(self.c_array_types)) + '\[[0-9]*\]'
        return '(' + built + types + built_arr + types_arr + ')'

    @staticmethod
    def escaped(array):
        """
        Escapes all the elements of the array
        
        :param array: list of types to escape 
        :return: list of types escaped
        """

        return list(map(re.escape, array))

    def _validate_source(self, tipo):
        """
        Validates if the type is from a source file
        
        :param tipo: str type to analyze
        :return: bool 
        """

        self.source_type = True
        self._get_source(tipo)
        return self.source_type

    def _validate_built_in(self, tipo):
        """
        Validates if the type is a built in type
        
        :param tipo: str type to anlyze 
        :return: bool
        """

        self.source_type = False
        self.source_file = "builtin"
        return tipo in self.c_built_ins or self._match_array(tipo, self.c_built_in_array_types)

    @staticmethod
    def _match_array(tipo, array):
        """
        Matches a regex with the type
        
        :param tipo: str type to match 
        :param array: regex to match
        :return: bool
        """

        return bool(re.match(array, tipo))

    def _get_source(self, tipo):
        """
        Gets the source file of the type received
        
        :param tipo: str type to find source 
        :return: None
        """

        if self._match_array(tipo, self.c_array_types):
            tipo = tipo.strip()[:-4]
        db = Database()
        query = "SELECT type_source FROM types WHERE type_name = '" + tipo + "' ORDER BY type_id"
        self.source_file = list(db.execute_query(query))
        if self.source_file:    # Validacion por si la query no encontro valores
            self.source_file = self.source_file[0][0]
        db.close_connection()

    def _get_types(self):
        """
        Gets all types from the database and adds their arrays types for regex
        
        :return: None 
        """

        db = Database()
        self.c_built_ins = list(map(lambda tup: tup[0], db.select_built_types()))
        self.c_built_in_array_types = r'^(' + '|'.join(self.escaped(self.c_built_ins)) + ')\[[0-9]*\]'
        self.c_types = list(map(lambda tup: tup[0], db.select_types()))
        self.c_array_types = r'^(' + '|'.join(self.escaped(self.c_types)) + ')\[[0-9]*\]'
        db.close_connection()
