import os
import sys
import errno
from socketpy.excpetions import ParseError, CreateError, CommandError, FileError
from socketpy.filing import Filer


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
        filer = Filer()
        filer.copy_files(models=True)
        filer._write_model(*args)
        return

    def _create_socket(self, *args):
        filer = Filer()
        filer.copy_files(sockets=True)
        filer._write_model(*args)
        return
