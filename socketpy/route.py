import sqlite3, os, re, sys
from socketpy.filing import FileLineWrapper
from socketpy.db import Database


class Route:

    def __init__(self):
        self.working_directory = os.getcwd()
        self.database = Database()

    # Public Interface #

    def create_route_table(self):
        self.database.create_routes_table()

    def load_route(self, directorios):
        route = os.sep.join(directorios)
        print("Ruta a insertar: ", route)
        self.database.insert_route(route)

    def flush_routes(self):
        self.database.flush_routes()

    def close_connection(self):
        self.database.close_connection()

    def _insert_route(self, route):
        self.database.insert_route(route)

