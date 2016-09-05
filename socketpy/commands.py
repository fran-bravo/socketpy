from socketpy.excpetions import CreateError, FileError, RouteError, HelpError, FlushError, EmbedError
from socketpy.filing import Filer
from socketpy.configure import Configure
from socketpy.db import Database
from socketpy.route import Route


def print_helpers(parser, key):
    if len(parser.helpers[key]) != 0:
        msg = "Las opciones para el comando " + key + " son: -"
        for opcion in parser.helpers[key]:
            msg += opcion + " "
    else:
        msg = "El comando no tiene opciones"
    return msg


class Command:

    def do_execute(self, parser, *args):
        pass


class HelpCommand(Command):
    commands = {}

    def __init__(self):
        self.commands = {'help': self, 'create': CreateCommand(),
                         'config': ConfigCommand(), 'flush': FlushCommand(),
                         'delete': DeleteCommand(), 'route': RouteCommand(),
                         'deconfig': DeconfigCommand(), 'reset': ResetCommand(),
                         'embed': EmbedCommand()}

    def do_execute(self, parser, *args):
        msg = ""
        if len(args[0]) == 0:
            msg = parser.msg_format_commands()
            print("Comandos disponibles: " + msg)
        elif args[0][0] in parser.commands:
            msg = str(self.commands[args[0][0]])
            msg += print_helpers(parser, args[0][0])
            print(msg)
        elif args[0][0] not in parser.commands:
            msg = "El comando ingresado no existe\nLos comandos disponibles son: "
            msg += parser.msg_format_commands()
            print(msg)
            raise HelpError(msg)
        return msg

    def __str__(self):
        return "El comando help permite ver una descripción explicativa de los comandos de socketpy\n"


class CreateCommand(Command):

    def __init__(self):
        self.filer = Filer()
        self.db = Database()

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += print_helpers(parser, "create")
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
        print("Escribiendo estructuras y funciones asociadas al modelo")
        model = self.filer.write_model(*args)
        print("Insertando modelo en base de datos")
        self.db.insert_type(model, "modelos.h")
        return

    def _create_socket(self, *args):
        self.filer.copy_templates()
        return

    def __str__(self):
        msg = "El comando create permite tanto inicializar la estructura de directorios necesario para el "
        msg += "uso de socketpy, así como crear modelos de estructuras utilizadas para el envío de datos por sockets\n"
        return msg


class ConfigCommand(Command):

    def do_execute(self, parser, *args):
        print("Configurando\n")
        conf = Configure()
        conf.initialize_directories()
        conf.create_db()
        conf.create_headers()
        conf.gather_types()
        conf.close_connection()

    def __str__(self):
        msg = "El comando config se encarga de analizar los archivos del proyecto, extraer "
        msg += "los tipos de datos con los que trabaja y encargarse de agregarlos a los datos "
        msg += "permitidos para la creación de modelos\n"
        return msg


class FlushCommand(Command):

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += "Las opciones para el comando flush son: -"
            for opcion in parser.helpers["flush"]:
                msg += opcion + " "
            raise FlushError(msg)
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
            raise FlushError(exc)

    def __str__(self):
        msg = "El comando flush elimina información particular de proyectos en los que se utilizó socketpy "
        msg += "anteriormente, ya sean tipos de datos o rutas\n"
        return msg


class DeleteCommand(Command):

    def __init__(self):
        self.filer = Filer()

    def do_execute(self, parser, *args):
        self.filer.delete_sockets()

    def __str__(self):
        msg = "El comando delete destruye el directorio de sockets en el que se ubican los sources de "
        msg += "socketpy\n"
        return msg


class RouteCommand(Command):

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += "Falta la ruta para el comando route"
            raise RouteError(msg)
        else:
            parameters = list(args)[0]
            router = Route()
            router.load_route(parameters)
            router.close_connection()

    def __str__(self):
        msg = "El comando route agrega una ruta en la que socketpy debe explorar para hallar archivos "
        msg += "sources que se utilizan en los #includes\n"
        return msg


class DeconfigCommand(Command):

    def do_execute(self, parser, *args):
        db = Database()
        print("Eliminando configuracion")
        db.destroy_database()

    def __str__(self):
        msg = "El comando deconfig elimina la base da datos que utiliza socketpy "
        msg += "(Existente por motivos de manejo entre versiones)\n"
        return msg


class ResetCommand(Command):

    def do_execute(self, parser, *args):
        db = Database()
        db.destroy_tables()
        db.create_tables()
        db.close_connection()

    def __str__(self):
        msg = "El comando reset reestablece la base de datos a su estado inicial "
        msg += "(Existente por motivos de facilidad de comprensión)\n"
        return msg


class EmbedCommand(Command):

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += "Se necesita tener un parámetro que especifique el tipo de dato y " \
                   "el archivo source al que pertenece"
            raise EmbedError(msg)
        else:
            parameters = list(args)[0]
            print(parameters)
            tipo = parameters.pop(0)
            source = parameters.pop(0)
        try:
            db = Database()
            db.insert_type(tipo, source)
            db.close_connection()
        except Exception as exc:
            raise EmbedError(exc)

    def __str__(self):
        msg = "El comando embed permite insertar un tipo de dato especifico "
        msg += "de forma manual y directa, con la finalidad de proveer un "
        msg += "mecanismo para agregar tipos que no se han detectado durante la configuracion\n"
        msg += "El formato para agregar tipos es [nombre_tipo] [archivo_source].\n"
        msg +="Ejemplo: socketpy embed t_log log.h\n"
        return msg