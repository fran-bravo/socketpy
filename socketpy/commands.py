from socketpy.excpetions import CreateError, FileError
from socketpy.filing import Filer
from socketpy.configure import Configure

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

    def do_execute(self, parser, *args):
        if len(args[0]) == 0:
            msg = "Faltan parametros\n"
            msg += "Las opciones para el comando help son: -"
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
        except FileError as exc:
            raise CreateError(exc)

    def _create_model(self, *args):
        self.filer.write_model(*args)
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