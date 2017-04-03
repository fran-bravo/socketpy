from unittest import TestCase
from socketpy.parser import Parser
from socketpy.exceptions import ParseError
import pytest, sys, io, os


class TestHelp(TestCase):
    parser = Parser()

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
        self.parser.parse(["create", "socket"])
        cwd = os.getcwd()
        subdirs = list(os.walk(cwd))[0][1]
        assert "sockets" in subdirs
