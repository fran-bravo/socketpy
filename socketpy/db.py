import sqlite3, os


class Database:

    def __init__(self):
        self.database = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database"), "types.db")
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_types_table(self):
        self.execute_query("""CREATE TABLE IF NOT EXISTS types (type_id INTEGER PRIMARY KEY,
                                type_name VARCHAR(50),
                                type_source VARCHAR(50))""")
        self.conn.commit()
        print("\tCreada tabla de tipos")

    def create_routes_table(self):
        self.execute_query("""CREATE TABLE IF NOT EXISTS routes (route_id INTEGER PRIMARY KEY,
                                route VARCHAR(100))""")
        self.conn.commit()
        print("\tCreada tabla de rutas")

    def execute_query(self, query):
        return self.cursor.execute(query)

    def select_built_types(self):
        return self.cursor.execute("""SELECT type_name FROM types WHERE type_source = 'builtin' ORDER BY type_id""")

    def select_types(self):
        return self.cursor.execute("""SELECT type_name FROM types WHERE type_source != 'builtin'  ORDER BY type_id""")

    def insert_type(self, tipo, source):
        if not self._validate_type(tipo):
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?)", (tipo, source))
            print("\tInsertado tipo de dato: ", tipo)
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?)", (tipo + "*", source))
            print("\tInsertado tipo de dato: ", tipo + "*")
            self.conn.commit()
        else:
            print("\tEl tipo de dato ya estaba en la base")

    def insert_route(self, route):
        if not self._validate_route(route):
            self.cursor.execute("INSERT INTO routes VALUES(NULL,?)", (route, ))
            print("\tInsertada ruta: ", route)
            self.conn.commit()
        else:
            print("\tLa ruta ya estaba en la base")

    def insert_types(self, types):
        if not self._validate_types(types):
            self.cursor.executemany("INSERT INTO types VALUES(NULL,?,?)", types)
            self.conn.commit()

    def flush_types(self):
        self.cursor.execute("""DELETE FROM types WHERE type_source != 'builtin';""")
        self.conn.commit()
        print("Eliminados registros de la tabla tipos")

    def flush_routes(self):
        self.cursor.execute("""DELETE FROM routes;""")
        self.conn.commit()
        print("Eliminados registros de la tabla rutas")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    #   Private Methods #

    def _validate_type(self, tipo):
        return tipo in self.get_types()

    def _validate_route(self, route):
        return route in self.get_routes()

    def _validate_types(self, types):
        type_names = list(map(lambda tup: tup[0], types))
        not_in_db = True
        for type in type_names:
            not_in_db = not_in_db and self._validate_type(type)
        return not_in_db

    def get_types(self):
        return list(map(lambda tup: tup[0], self.cursor.execute(
                    "SELECT type_name FROM types ORDER BY type_id")))

    def get_routes(self):
        return list(map(lambda tup: tup[0], self.cursor.execute(
            "SELECT route FROM routes ORDER BY route_id")))

    def destroy_database(self):
        self.close_connection()
        os.remove(self.database)
        return
