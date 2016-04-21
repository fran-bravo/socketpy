import os
import sys
import errno

class Parser:

    def __init__(self):
        self.commands = {'help': self.parser_help, 'create': self.create}

    # Public Interface

    # Commands

    def parser_help(self, *args):
        msg = self._msg_format_commands()
        print("Comandos disponibles: " + msg)
        return msg

    def create(self, *args):
        if len(args[0]) == 0:
            msg = ["Faltan parametros"]
            raise CreateError(' - '.join(msg))
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

    # Parse

    def parse(self, *args):
        if len(args[0]) == 0:
            msg = ["Te olvidaste el comando? Los comandos son: "]
            msg.append(self._msg_format_commands())
            raise CommandError(' - '.join(msg))
        else:
            parameters = list(args)[0]
            command = parameters.pop(0)

        try:
            return self.commands[command](*args)
        except KeyError:
            msg = ['Unknown command "%s"' % command]
            raise CommandError(' - '.join(msg))

    # Private Methods

    def _msg_format_commands(self):
        comandos = self._get_commands()
        msg = " , ".join(comandos)
        return msg

    def _get_commands(self):
        return self.commands.keys()

    def _create_model(self, *args):
        path = os.path.dirname(os.path.abspath(__file__)) + "/modelos"
        if not os.path.exists(path):
            os.mkdir(path)

        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

        try:
            file_handle = os.open('modelos/modelos.h', flags)
        except OSError as e:
            raise FileError("???")
        else:  # No exception, so the file must have been created successfully.
            with os.fdopen(file_handle, 'w') as file_obj:
                file_obj.write("Look, ma, I'm writing to a new file!")
        # TODO
        return

    def _create_socket(self, *args):
        # TODO
        return

class ParseError(Exception):
    """Base socketpy exception"""


class CommandError(ParseError):
    pass


class CreateError(CommandError):
    pass


class FileError(CreateError):
    pass