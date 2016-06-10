import re, os, sqlite3
from socketpy.db import Database


class Analyzer:
    c_built_ins = []
    c_types = []
    c_built_in_array_types = r'^[' + '|'.join(c_built_ins) + ']'
    c_array_types = []

    def __init__(self):
        self._get_types()
        self.source_type = False
        self.source_file = ""

    def analyze_type(self, tipo):
        if tipo in self.c_types or self._match_array(tipo, self.c_array_types):
            self.source_type = True
            self._get_source(tipo)
            return self.source_type
        else:
            self.source_type = False
            self.source_file = "builtin"
            return tipo in self.c_built_ins or self._match_array(tipo, self.c_built_in_array_types)

    @staticmethod
    def _match_array(tipo, array):
        if re.match(array, tipo) and re.match('^\\[[0-9]+\\]', tipo[-4:]):
            return True
        else:
            return False

    def _get_source(self, tipo):
        db = Database()
        query = "SELECT type_source FROM types WHERE type_name = '" + tipo + "' ORDER BY type_id"
        self.source_file = list(db.execute_query(query))[0][0]
        db.close_connection()

    def _get_types(self):
        db = Database()
        self.c_built_ins = list(map(lambda tup: tup[0], db.select_built_types()))
        self.c_built_in_array_types = r'^[' + '|'.join(self.c_built_ins) + ']'
        self.c_types = list(map(lambda tup: tup[0], db.select_types()))
        self.c_array_types = r'^[' + '|'.join(self.c_types) + ']'
        db.close_connection()

