import sqlite3, os


class Database:

    def __init__(self):
        self.database = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database"), "types.db")
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS types (type_id INTEGER PRIMARY KEY,
                                type_name VARCHAR(50),
                                type_built_in BIT,
                                type_source VARCHAR(50))""")
        self.conn.commit()

    def execute_query(self, query):
        return self.cursor.execute(query)

    def select_built_types(self):
        return self.cursor.execute("""SELECT type_name FROM types WHERE type_built_in = 1 ORDER BY type_id""")

    def select_types(self):
        return self.cursor.execute("""SELECT type_name FROM types WHERE type_built_in = 0 ORDER BY type_id""")

    def insert_type(self, tipo, source):
        print(source)
        if not self._validate_type(tipo):
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?,?)", (tipo, 0, source))
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?,?)", (tipo + "*", 0, source))
            self.conn.commit()

    def insert_types(self, types):
        if not self._validate_types(types):
            self.cursor.executemany("INSERT INTO types VALUES(NULL,?,?,?)", types)
            self.conn.commit()

    def flush_db(self):
        self.cursor.execute("""DELETE FROM types WHERE type_built_in = 0;""")
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def _validate_type(self, tipo):
        c_built_ins = list(map(lambda tup: tup[0], self.cursor.execute(
            'SELECT type_name FROM types WHERE type_built_in = 1 ORDER BY type_id')))
        return tipo in c_built_ins

    def _validate_types(self, types):
        c_built_ins = list(map(lambda tup: tup[0], self.cursor.execute(
            'SELECT type_name FROM types WHERE type_built_in = 1 ORDER BY type_id')))

        type_names = list(map(lambda tup: tup[0], types))
        return type_names == c_built_ins
