import pytest, sys, io, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from unittest import TestCase
from socketpy.configure import Configure
from socketpy.db import Database


class TestConfigure(TestCase):
    configurer = Configure()

    def setUp(self):
        db = Database()
        self.configurer = Configure()
        self.configurer.initialize_directories()
        self.configurer.create_db()
        self.configurer.create_headers()
        self.configurer.gather_types()

    def tearDown(self):
        self.configurer.database.destroy_database()

    def test_typedef_end(self):
        self.configurer._get_type_from_typedef_end_sentence("} __attribute__ ((__packed__)) t_persona;", "modelos.h")
        types = self.configurer.database.get_types()
        assert "t_persona" in types

    def test_typedef_basic_puntero(self):
        self.configurer._get_type_from_typedef_sentence("typedef void (*functionVoid)(void);", "modelos.h")
        types = self.configurer.database.get_types()
        assert "functionVoid" in types

    def test_typedef_basic_struct(self):
        self.configurer._get_type_from_typedef_sentence("typedef struct _IO_FILE FILE;", "modelos.h")
        types = self.configurer.database.get_types()
        assert "FILE" in types

    def test_typedef_basic(self):
        self.configurer._get_type_from_typedef_sentence("typedef uint8_t int8;", "modelos.h")
        types = self.configurer.database.get_types()
        assert "int8" in types
