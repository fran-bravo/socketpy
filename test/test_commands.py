import pytest, sys, io, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from unittest import TestCase
from socketpy.parser import Parser
from socketpy.exceptions import ParseError, CreateError, FlushError, RouteError, EmbedError
from socketpy.filing import FileLineWrapper
from socketpy.db import Database
from socketpy.commands import print_helpers


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

    def test_command_help(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help"])
            output = out.getvalue().strip()
            msg = "Comandos disponibles: "
            msg += self.parser.msg_format_commands()
            assert output == msg
        finally:
            sys.stdout = saved_stdout

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
            finally:
                sys.stderr = saved_stdout

    def test_command_help_create(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "create"])
            output = out.getvalue().strip()
            msg = "El comando create permite tanto inicializar la estructura de directorios necesario para el "
            msg += "uso de socketpy, así como crear modelos de estructuras utilizadas para el envío de datos por sockets\n"
            msg += print_helpers(self.parser, 'create')
            msg = msg[:-1]
            assert output == msg
        finally:
            sys.stdout = saved_stdout

    def test_command_help_config(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "config"])
            output = out.getvalue().strip()
            msg = "El comando config se encarga de analizar los archivos del proyecto, extraer "
            msg += "los tipos de datos con los que trabaja y encargarse de agregarlos a los datos "
            msg += "permitidos para la creación de modelos\n"
            msg += print_helpers(self.parser, 'config')
            assert output == msg
        finally:
            sys.stdout = saved_stdout

    def test_command_help_flush(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "flush"])
            output = out.getvalue().strip()
            msg = "El comando flush elimina información particular de proyectos en los que se utilizó socketpy "
            msg += "anteriormente, ya sean tipos de datos o rutas\n"
            msg += print_helpers(self.parser, 'flush')
            msg = msg[:-1]
            assert output == msg
        finally:
            sys.stdout = saved_stdout

    def test_command_help_embed(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "embed"])
            output = out.getvalue().strip()
            msg = "El comando embed permite insertar un tipo de dato especifico "
            msg += "de forma manual y directa, con la finalidad de proveer un "
            msg += "mecanismo para agregar tipos que no se han detectado durante la configuracion\n"
            msg += "El formato para agregar tipos es [nombre_tipo] [archivo_source].\n"
            msg += "Ejemplo: socketpy embed t_log log.h\n"
            msg += print_helpers(self.parser, 'embed')
            assert output == msg
        finally:
            sys.stdout = saved_stdout

    def test_command_help_reset(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "reset"])
            output = out.getvalue().strip()
            msg = "El comando reset reestablece la base de datos a su estado inicial "
            msg += "(Existente por motivos de facilidad de comprensión)\n"
            msg += print_helpers(self.parser, 'reset')
            assert output == msg
        finally:
            sys.stdout = saved_stdout

    def test_command_help_deconfig(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "deconfig"])
            output = out.getvalue().strip()
            msg = "El comando deconfig elimina la base de datos que utiliza socketpy "
            msg += "y elimina la carpeta de sockets "
            msg += "(Existente por motivos de manejo entre versiones)\n"
            msg += print_helpers(self.parser, 'deconfig')
            assert output == msg
        finally:
            sys.stdout = saved_stdout

    def test_command_help_route(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "route"])
            output = out.getvalue().strip()
            msg = "El comando route agrega una ruta en la que socketpy debe explorar para hallar archivos "
            msg += "sources que se utilizan en los #includes\n"
            msg += print_helpers(self.parser, 'route')
            assert output == msg
        finally:
            sys.stdout = saved_stdout

    def test_command_help_delete(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            self.parser.parse(["help", "delete"])
            output = out.getvalue().strip()
            msg = "El comando delete destruye el directorio de sockets en el que se ubican los sources de "
            msg += "socketpy\n"
            msg += print_helpers(self.parser, 'delete')
            assert output == msg
        finally:
            sys.stdout = saved_stdout

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

    def test_command_reset(self):
        self.parser.parse(["reset"])

        db = Database()
        types = db.get_types()

        assert types == []

#   Errors  #

    def test_command_create_wrong_parameter(self):
        with pytest.raises(CreateError):
            self.parser.parse(["create", "database"])

    def test_command_create_missing_parameters(self):
        with pytest.raises(CreateError):
            self.parser.parse(["create"])

    def test_command_flush_missing_parameters(self):
        with pytest.raises(FlushError):
            self.parser.parse(["flush"])

    def test_command_flush_wrong_parameter(self):
        with pytest.raises(FlushError):
            self.parser.parse(["flush", "database"])

    def test_command_route_missing_parameter(self):
        with pytest.raises(RouteError):
            self.parser.parse(["route"])

    def test_command_embed_missing_parameter(self):
        with pytest.raises(EmbedError):
            self.parser.parse(["embed"])
