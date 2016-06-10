import sqlite3, os


class Database:

    def __init__(self):
        self.database = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database"), "types.db")
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS types (type_id INTEGER PRIMARY KEY,
                                type_name VARCHAR(50),
                                type_source VARCHAR(50))""")
        self.conn.commit()

    def execute_query(self, query):
        return self.cursor.execute(query)

    def select_built_types(self):
        return self.cursor.execute("""SELECT type_name FROM types WHERE type_source = 'builtin' ORDER BY type_id""")

    def select_types(self):
        return self.cursor.execute("""SELECT type_name FROM types WHERE type_source != 'builtin'  ORDER BY type_id""")

    def insert_type(self, tipo, source):
        if not self._validate_type(tipo):
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?)", (tipo, source))
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?)", (tipo + "*", source))
            self.conn.commit()
            print("\tInsertado tipo de dato: ", tipo)

    def insert_types(self, types):
        if not self._validate_types(types):
            self.cursor.executemany("INSERT INTO types VALUES(NULL,?,?)", types)
            self.conn.commit()

    def flush_db(self):
        self.cursor.execute("""DELETE FROM types WHERE type_source != 'builtin';""")
        self.conn.commit()
        print("Eliminados registros de la base de datos")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def _validate_type(self, tipo):
        c_built_ins = self._get_types()
        return tipo in c_built_ins

    def _validate_types(self, types):
        type_names = list(map(lambda tup: tup[0], types))
        not_in_db = True
        for type in type_names:
            not_in_db = not_in_db and self._validate_type(type)
        return not_in_db

    def _get_types(self):
        return list(map(lambda tup: tup[0], self.cursor.execute(
                    "SELECT type_name FROM types ORDER BY type_id")))
