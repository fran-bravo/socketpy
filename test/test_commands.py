from unittest import TestCase
from socketpy.parser import Parser
from socketpy.exceptions import ParseError
from socketpy.filing import FileLineWrapper
from socketpy.db import Database
import pytest, sys, io, os


INCLUDES = "/usr/include"
LIBS = "/usr/lib"


class TestCommands(TestCase):
    parser = Parser()

    def _init_socketpy(self):
        self.parser.parse(["config"])
        self.parser.parse(["create", "socket"])

    def _destroy_socketpy(self):
        self.parser.parse(['deconfig'])

    def test_command_help(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "help"])
            output = out.getvalue().strip()
            assert output == 'El comando help permite ver una descripción explicativa de los comandos de socketpy\nEl comando no tiene opciones'
        finally:
            sys.stdout = saved_stdout

    def test_command_help_unknown_error(self):
        with pytest.raises(ParseError):
            saved_stdout = sys.stdout
            try:
                out = io.StringIO()
                sys.stderr = out
                self.parser.parse(["help", "asda"])
                output = out.getvalue().strip()
                assert output == 'El comando ingresado no existe\nLos comandos disponibles son: config, create, delete, flush, help, route\nERROR: Unknown command "help"'
            finally:
                sys.stderr = saved_stdout

    def test_command_create_socket(self):
        try:
            self._init_socketpy()
            cwd = os.getcwd()
            print("Directory {}".format(cwd))
            subdirs = list(os.walk(cwd))[0][1]
            assert "sockets" in subdirs
        finally:
            self._destroy_socketpy()

    def test_command_create_model(self):
        try:
            self._init_socketpy()
            self.parser.parse(["create", "model", "persona", "dni:int", "nombre:char*", "edad:int"])
            cwd = os.getcwd()
            path = os.path.join(os.path.join(cwd, "sockets"), "modelos.h")
            fd = FileLineWrapper(open(path, "r"))

            assert any(list(map(lambda line: "persona" in line, fd.f)))
        finally:
            fd.close()
            self._destroy_socketpy()

    def test_command_create_model_update(self):
        try:
            self._init_socketpy()
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
            self._destroy_socketpy()

    def test_command_route(self):
        try:
            self._init_socketpy()
            self.parser.parse(["route", "/usr/include"])
            db = Database()
            routes = db.get_routes()

            assert "/usr/include" in routes
        finally:
            self._destroy_socketpy()

    def test_command_flush_route(self):
        try:
            self._init_socketpy()
            self.parser.parse(["route", "/usr/include"])
            self.parser.parse(["flush", "routes"])
            db = Database()
            routes = db.get_routes()

            assert routes == []
        finally:
            db.close_connection()
            self._destroy_socketpy()

    def test_command_flush_types(self):
        try:
            self._init_socketpy()
            self.parser.parse(["flush", "types"])
            db = Database()
            types = db.get_types()

            assert "t_stream" not in types
        finally:
            db.close_connection()
            self._destroy_socketpy()

    def test_command_embed(self):
        try:
            self._init_socketpy()
            self.parser.parse(["embed", "t_prueba", "prueba.h"])
            db = Database()
            types = db.get_types()

            assert "t_prueba" in types
        finally:
            db.close_connection()
            self._destroy_socketpy()

    def test_command_compile(self):
        try:
            self._init_socketpy()
            self.parser.parse(["create", "model", "persona", "dni:int", "nombre:char*", "edad:int"])
            self.parser.parse(["compile"])

            paquetes = os.path.join(INCLUDES, "paquetes.h")
            modelos = os.path.join(INCLUDES, "modelos.h")
            library = os.path.join(LIBS, "libsockets.so")

            assert os.path.exists(paquetes)
            assert os.path.exists(modelos)
            assert os.path.exists(library)
        finally:
            self._destroy_socketpy()
