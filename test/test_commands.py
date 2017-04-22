import pytest, sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from unittest import TestCase
from socketpy.parser import Parser
from socketpy.filing import FileLineWrapper
from socketpy.db import Database


INCLUDES = "/usr/include"
LIBS = "/usr/lib"


class TestCommands(TestCase):
    parser = Parser()

    def setUp(self):
        self.parser.parse(["config"])
        self.parser.parse(["create", "socket"])

    def tearDown(self):
        self.parser.parse(['delete'])
        self.parser.parse(['deconfig'])

    def test_command_create_socket(self):
        cwd = os.getcwd()
        subdirs = list(os.walk(cwd))[0][1]

        assert "sockets" in subdirs

    def test_command_create_model(self):
        try:
            self.parser.parse(["create", "model", "persona", "dni:int", "nombre:char*", "edad:int"])
            cwd = os.getcwd()
            path = os.path.join(os.path.join(cwd, "sockets"), "modelos.h")
            fd = FileLineWrapper(open(path, "r"))

            assert any(list(map(lambda line: "persona" in line, fd.f)))
        finally:
            fd.close()

    def test_command_create_model_update(self):
        try:
            self.parser.parse(["create", "model", "persona", "dni:int", "nombre:char*", "edad:int"])
            self.parser.parse(["create", "model", "persona", "dni:int", "nombre:char*", "edad:int", "hijo:persona"])
            cwd = os.getcwd()
            path = os.path.join(os.path.join(cwd, "sockets"), "modelos.h")
            fd1 = FileLineWrapper(open(path, "r"))
            fd2 = FileLineWrapper(open(path, "r"))

            assert any(list(map(lambda line: "persona" in line, fd1.f)))
            assert any(list(map(lambda line: "hijo" in line, fd2.f)))
        finally:
            fd1.close()
            fd2.close()

    def test_command_route(self):
        self.parser.parse(["route", "/usr/include"])
        db = Database()
        routes = db.get_routes()

        assert "/usr/include" in routes

    def test_command_config_with_route(self):
        self.parser.parse(["route", "/usr/include"])
        self.parser.parse(["config"])
        db = Database()
        types = db.get_types()

        assert "FILE" in types

    def test_command_flush_route(self):
        try:
            self.parser.parse(["route", "/usr/include"])
            self.parser.parse(["flush", "routes"])
            db = Database()
            routes = db.get_routes()

            assert routes == []
        finally:
            db.close_connection()

    def test_command_flush_types(self):
        try:
            self.parser.parse(["flush", "types"])
            db = Database()
            types = db.get_types()

            assert "t_stream" not in types
        finally:
            db.close_connection()

    def test_command_embed(self):
        try:
            self.parser.parse(["embed", "t_prueba", "prueba.h"])
            db = Database()
            types = db.get_types()

            assert "t_prueba" in types
        finally:
            db.close_connection()

    def test_command_compile(self):
        self.parser.parse(["create", "model", "persona", "dni:int", "nombre:char*", "edad:int"])
        self.parser.parse(["compile"])

        paquetes = os.path.join(INCLUDES, "paquetes.h")
        modelos = os.path.join(INCLUDES, "modelos.h")
        library = os.path.join(LIBS, "libsockets.so")

        assert os.path.exists(paquetes)
        assert os.path.exists(modelos)
        assert os.path.exists(library)

    def test_command_decompile(self):
        self.parser.parse(["create", "model", "persona", "dni:int", "nombre:char*", "edad:int"])
        self.parser.parse(["compile"])
        self.parser.parse(["decompile"])

        paquetes = os.path.join(INCLUDES, "paquetes.h")
        modelos = os.path.join(INCLUDES, "modelos.h")
        library = os.path.join(LIBS, "libsockets.so")

        assert not os.path.exists(paquetes)
        assert not os.path.exists(modelos)
        assert not os.path.exists(library)

    def test_command_reset(self):
        self.parser.parse(["reset"])

        db = Database()
        types = db.get_types()

        assert types == []
