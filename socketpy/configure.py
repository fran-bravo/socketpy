import sqlite3, os
from socketpy.excpetions import FileError
from socketpy.filing import Filer


class Configure:

    def __init__(self):
        self.working_directory = os.getcwd()
        self._create_directory()
        self.database = os.path.dirname(os.path.abspath(__file__)) + "\\database\\types.db"
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        self.create_db()

    def create_db(self):
        self.cursor.execute("""CREATE TABLE types (type_id INTEGER PRIMARY KEY,
                                                   type_name VARCHAR(50),
                                                   type_built_in BIT)""")
        self._load_basic_types()
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def _load_basic_types(self):
        types = [("int", 1), ("uint8_t", 1),
                 ("uint16_t", 1), ("uint32_t", 1),
                 ("void", 1), ("char", 1),
                 ("int*", 1), ("uint8_t*", 1),
                 ("uint16_t*", 1), ("uint32_t*", 1),
                 ("void*", 1), ("char*", 1),
                 ]
        self.cursor.executemany("INSERT INTO types VALUES(NULL, ?,?)", types)

    @staticmethod
    def _create_directory():
        if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "\\database"):
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + "\\database")

