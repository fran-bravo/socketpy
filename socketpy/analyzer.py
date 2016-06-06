import re, os, sqlite3


class Analyzer:
    c_built_ins = []
    c_array_types = r'^[' + '|'.join(c_built_ins) + ']'

    def __init__(self):
        self._get_types()

    def analyze_type(self, tipo):
        print(self.c_array_types)
        return tipo in self.c_built_ins or self._match_array(tipo)

    def _match_array(self, tipo):
        if re.match(self.c_array_types, tipo) and re.match('^\\[[0-9]+\\]', tipo[-4:]):
            return True
        else:
            return False

    def _get_types(self):
        database = os.path.dirname(os.path.abspath(__file__)) + "\\database\\types.db"
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        self.c_built_ins = list(map(lambda tup: tup[0], cursor.execute('SELECT type_name FROM types WHERE type_built_in = 1 ORDER BY type_id')))
        self.c_array_types = r'^[' + '|'.join(self.c_built_ins) + ']'
        cursor.close()
        conn.close()

