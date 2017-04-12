import re, os, sqlite3
from dbus import types
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
        if not self.c_types:
            return self._validate_built_in(tipo)
        else:
            if tipo in self.c_types or self._match_array(tipo, self.c_array_types):
                return self._validate_source(tipo)
            else:
                return self._validate_built_in(tipo)

    def all(self):
        built = '|'.join(self.escaped(self.c_built_ins))
        print(built)
        types = '|'.join(self.escaped(self.c_types))
        built_arr = '|'.join(self.escaped(self.c_built_ins)) + '\[[0-9]*\]'
        types_arr = '|'.join(self.escaped(self.c_types)) + '\[[0-9]*\]'
        return '(' + built + types + built_arr + types_arr + ')'

    @staticmethod
    def escaped(array):
        return list(map(re.escape, array))

    def examine(self):
        print(self.c_built_ins)
        print(self.c_built_in_array_types)
        print(self.c_types)
        print(self.c_array_types)

    def _validate_source(self, tipo):
        self.source_type = True
        print("Tipo {}".format(tipo))
        self._get_source(tipo)
        print("Source {}".format(self.source_file))
        return self.source_type or self._match_array(tipo, self.c_array_types)

    def _validate_built_in(self, tipo):
        self.source_type = False
        self.source_file = "builtin"
        return tipo in self.c_built_ins or self._match_array(tipo, self.c_built_in_array_types)

    @staticmethod
    def _match_array(tipo, array):
        if re.match(array, tipo):
            return True
        else:
            return False

    def _get_source(self, tipo):
        if self._match_array(tipo, self.c_array_types):
            tipo = tipo[:-5]
        db = Database()
        query = "SELECT type_source FROM types WHERE type_name = '" + tipo + "' ORDER BY type_id"
        self.source_file = list(db.execute_query(query))
        if self.source_file:    # Validacion por si la query no encontro valores
            self.source_file = self.source_file[0][0]
        db.close_connection()

    def _get_types(self):
        db = Database()
        self.c_built_ins = list(map(lambda tup: tup[0], db.select_built_types()))
        self.c_built_in_array_types = r'^(' + '|'.join(self.c_built_ins) + ')\[[0-9]*\]'
        self.c_types = list(map(lambda tup: tup[0], db.select_types()))
        self.c_array_types = r'^(' + '|'.join(self.c_types) + ')\[[0-9]*\]'
        db.close_connection()
