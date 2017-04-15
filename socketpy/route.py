import sqlite3, os, re, sys
from socketpy.filing import FileLineWrapper
from socketpy.db import Database


class Route:

    def __init__(self):
        self.working_directory = os.getcwd()
        self.database = Database()

    # Public Interface #

    def load_route(self, directorios):
        """
        Formats the route and inserts it in the database
        
        :param directorios: str with the route to add 
        :return: None
        """

        route = os.sep.join(directorios)
        print("Ruta a insertar: ", route)
        self._insert_route(route)

    def flush_routes(self):
        """
        Deletes the routes in the database
        
        :return: None 
        """

        self.database.flush_routes()

    def close_connection(self):
        """
        Closes the connection to the database
        
        :return: None 
        """

        self.database.close_connection()

    def _insert_route(self, route):
        """
        Inserts the route in the database
        
        :param route: str with the route 
        :return: None
        """

        self.database.insert_route(route)

