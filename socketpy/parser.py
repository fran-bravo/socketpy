import os
import sys
import errno
from socketpy.excpetions import ParseError, CommandError, FileError
from socketpy.filing import Filer
from socketpy.commands import HelpCommand, CreateCommand, ConfigCommand


class Parser:

    def __init__(self):
        self.commands = {'help': self.parser_help, 'create': self.create, 'config': self.config}
        self.helpers = {'help': [], 'create': ['model', 'socket']}

    # Public Interface

    # Commands

    def parser_help(self, *args):
        HelpCommand().do_execute(self, *args)
        return "help"

    def create(self, *args):
        CreateCommand().do_execute(self, *args)
        return "create"

    def config(self, *args):
        ConfigCommand().do_execute(self, *args)
        return "config"

    # Parse

    def parse(self, *args):
        if len(args[0]) == 0:
            msg = ["¿Te olvidaste el comando? Los comandos son: "]
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
