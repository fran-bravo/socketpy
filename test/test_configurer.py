import pytest, sys, io, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from unittest import TestCase
from socketpy.configure import Configure
from socketpy.db import Database


class TestConfigure(TestCase):
    configurer = Configure()

    def _init_configure(self):
        db = Database()
        self.configurer.initialize_directories()
        self.configurer.create_db()
        self.configurer.create_headers()
        self.configurer.gather_types()

    def _destroy_configure(self):
        self.configurer.database.destroy_database()

    def test_typedef_end(self):
        try:
            self._init_configure()
            self.configurer._get_type_from_typedef_end_sentence("} __attribute__ ((__packed__)) t_persona;", "modelos.h")
            types = self.configurer.database.get_types()
            print("Tipos {}".format(types))
            assert "t_persona" in types
        finally:
            self._destroy_configure()
