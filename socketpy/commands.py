import sqlite3
from socketpy.excpetions import CreateError, FileError, RouteError
from socketpy.filing import Filer
from socketpy.configure import Configure
from socketpy.db import Database
from socketpy.route import Route

class Command():

    def do_execute(self, parser, *args):
        pass


class HelpCommand(Command):

    def do_execute(self, parser, *args):
        msg = ""
        if len(args[0]) == 0:
            msg = parser._msg_format_commands()
            print("Comandos disponibles: " + msg)
        elif args[0][0] in parser.commands:
            msg = "Las opciones para el comando help son: "
            for opcion in parser.helpers["help"]:
                msg += opcion + " "
            print(msg)
        return msg


class CreateCommand(Command):

    def __init__(self):
        self.filer = Filer()
        self.db = Database()

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += "Las opciones para el comando create son: -"
            for opcion in parser.helpers["create"]:
                msg += opcion + " "
            raise CreateError(msg)
        else:
            parameters = list(args)[0]
            tipo = parameters.pop(0)
        try:
            if tipo.lower() == "model":
                self._create_model(parameters)
            elif tipo.lower() == "socket":
                self._create_socket(parameters)
            else:
                msg = "Opcion invalida para el comando create"
                raise CreateError(msg)
        except FileError as exc:
            raise CreateError(exc)

    def _create_model(self, *args):
        print("Escribiendo estructuras y funcoines asociadas al modelo")
        model = self.filer.write_model(*args)
        print("Insertando modelo en base de datos")
        self.db.insert_type(model, "modelos.h")
        return

    def _create_socket(self, *args):
        self.filer.copy_templates()
        return


class ConfigCommand(Command):

    def do_execute(self, parser, *args):
        print("Configurando\n")
        conf = Configure()
        conf.initialize_directories()
        conf.create_db()
        conf.create_headers()
        conf.gather_types()
        conf.close_connection()


class FlushCommand(Command):

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += "Las opciones para el comando flush son: -"
            for opcion in parser.helpers["flush"]:
                msg += opcion + " "
            raise CreateError(msg)
        else:
            parameters = list(args)[0]
            tipo = parameters.pop(0)
        try:
            if tipo.lower() == "types":
                db = Database()
                db.flush_types()
                db.close_connection()
            elif tipo.lower() == "routes":
                db = Database()
                db.flush_routes()
                db.close_connection()
        except FileError as exc:
            raise CreateError(exc)


class DeleteCommand(Command):

    def __init__(self):
        self.filer = Filer()

    def do_execute(self, parser, *args):
        self.filer.delete_sockets()


class RouteCommand(Command):

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += "Falta la ruta para el comando route"
            raise RouteError(msg)
        else:
            parameters = list(args)[0]
            router = Route()
            router.create_route_table()
            router.load_route(parameters)
            router.close_connection()
