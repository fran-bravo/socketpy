import sqlite3, os
import shutil


class Database:

    def __init__(self):
        self.database = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database"), "types.db")
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database"))
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        Creates the tables used by socketpy
        
        :return: None 
        """

        print("Creando tablas")
        self._create_types_table()
        self.create_routes_table()

    def execute_query(self, query):
        """
        Executes a query on the cursor of the db
        
        :param query: str of the query to be executed 
        :return: sqlite3.Cursor with the result of the query
        """

        return self.cursor.execute(query)

    def select_built_types(self):
        """
        Executes a select query which obtains built_in types
        
        :return: sqlite3.Cursor with the result of the query 
        """

        return self.cursor.execute("""SELECT type_name FROM types WHERE type_source = 'builtin' ORDER BY type_id""")

    def select_types(self):
        """
        Executes a select query which obtains non built_in types

        :return: sqlite3.Cursor with the result of the query 
        """

        return self.cursor.execute("""SELECT type_name FROM types WHERE type_source != 'builtin'  ORDER BY type_id""")

    def insert_type(self, tipo, source):
        """
        Validates if tipo is a type in the database and if not, it inserts it along with a ptr version of it
        
        :param tipo: str of the type to be inserted
        :param source: str with the source file of the type tipo
        :return: None
        """

        if not self._validate_type(tipo):
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?)", (tipo, source))
            print("\tInsertado tipo de dato: ", tipo)
            self.cursor.execute("INSERT INTO types VALUES(NULL,?,?)", (tipo + "*", source))
            print("\tInsertado tipo de dato: ", tipo + "*")
            self.conn.commit()
        else:
            print("\tEl tipo de dato: %s ya estaba en la base" % tipo)

    def insert_route(self, route):
        """
        Validates if route is already in the database and if not, it inserts it
        
        :param route: str with the route to be inserted 
        :return: None
        """

        if not self._validate_route(route):
            self.cursor.execute("INSERT INTO routes VALUES(NULL,?)", (route, ))
            print("\tInsertada ruta: ", route)
            self.conn.commit()
        else:
            print("\tLa ruta ya estaba en la base")

    def insert_types(self, types):
        """
        Inserts a group of types as built ins, with previous validation of already in database
        
        :param types: list of types to be inserted
        :return: None
        """

        if not self._validate_types(types):
            self.cursor.executemany("INSERT INTO types VALUES(NULL,?,?)", types)
            self.conn.commit()

    def flush_types(self):
        """
        Deletes all non built in types from the database
        
        :return: None 
        """

        self.cursor.execute("""DELETE FROM types WHERE type_source != 'builtin';""")
        self.conn.commit()
        print("Eliminados registros de la tabla tipos")

    def flush_routes(self):
        """
        Deletes all the routes from the database
        
        :return: None
        """

        self.cursor.execute("""DELETE FROM routes;""")
        self.conn.commit()
        print("Eliminados registros de la tabla rutas")

    def close_connection(self):
        """
        Closes the cursor and the conection with the database
        
        :return: None
        """

        self.cursor.close()
        self.conn.close()

    def get_types(self):
        """
        Gets all the types of the database ordered by id
        
        :return: list of the types in the database
        """

        return list(map(lambda tup: tup[0], self.cursor.execute(
                    "SELECT type_name FROM types ORDER BY type_id")))

    def get_routes(self):
        """
        Gets all the routes of the database ordered by id
        
        :return: list of all the routes in the database 
        """

        return list(map(lambda tup: tup[0], self.cursor.execute(
            "SELECT route FROM routes ORDER BY route_id")))

    def destroy_database(self):
        """
        Closes the connection and deletes the database file
        
        :return: None 
        """

        self.close_connection()
        print("\tDesconectada base de datos")
        os.remove(self.database)
        shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database"))
        print("\tEliminada base de datos")

    def destroy_tables(self):
        """
        Destroys both tables of the database
        
        :return: None 
        """

        print("Destruyendo tablas")
        self._destroy_table("types")
        self._destroy_table("routes")

    #   Private Methods #

    def _validate_type(self, tipo):
        """
        Validates if tipo is a type in the database
        
        :param tipo: str of a type 
        :return: bool 
        """

        return tipo in self.get_types()

    def _validate_route(self, route):
        """
        Validates if route is already in the database
         
        :param route: str of a route 
        :return: bool
        """

        return route in self.get_routes()

    def _validate_types(self, types):
        """
        Validates if a list of types is already in the database
        
        :param types: list of types 
        :return: bool
        """

        type_names = list(map(lambda tup: tup[0], types))
        not_in_db = True
        for type in type_names:
            not_in_db = not_in_db and self._validate_type(type)
        return not_in_db

    def _destroy_table(self, tabla):
        """
        Drops the table named tabla from the database
        
        :param tabla: str with the name of the table 
        :return: None
        """

        self.execute_query("""DROP TABLE IF EXISTS %s;""" % tabla)
        self.conn.commit()
        print("\tTabla %s destruida" % tabla)

    def _create_types_table(self):
        """
        Creates types table
        
        :return: None 
        """

        self.execute_query("""CREATE TABLE IF NOT EXISTS types (type_id INTEGER PRIMARY KEY,
            type_name VARCHAR(50),
            type_source VARCHAR(50))""")
        print("\tCreada tabla de tipos")

    def create_routes_table(self):
        """
        Creates routes table
        
        :return: None 
        """

        self.execute_query("""CREATE TABLE IF NOT EXISTS routes (route_id INTEGER PRIMARY KEY,
                                route VARCHAR(100))""")
        self.conn.commit()
        print("\tCreada tabla de rutas")
