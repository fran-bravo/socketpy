from socketpy.excpetions import CommandError, ParseError, SOCKETPY_ERRORS
from socketpy.commands import HelpCommand, CreateCommand, ConfigCommand, FlushCommand, DeleteCommand, RouteCommand


class Parser:

    def __init__(self):
        self.commands = {'help': self.parser_help, 'create': self.create,
                         'config': self.config, 'flush': self.flush,
                         'delete': self.delete, 'route': self.route}
        self.helpers = {'help': [], 'create': ['model', 'socket'], 'config': [],
                        'flush': ['types', 'routes'], 'delete': [], 'route': []}

    # Public Interface

    # Commands

    def parser_help(self, *args):
        HelpCommand().do_execute(self, *args)
        return "help"

    def create(self, *args):
        CreateCommand().do_execute(self, *args)
        return "create"

    def delete(self, *args):
        DeleteCommand().do_execute(self, *args)
        return "delete"

    def route(self, *args):
        RouteCommand().do_execute(self, *args)
        return "route"

    def config(self, *args):
        ConfigCommand().do_execute(self, *args)
        return "config"

    def flush(self, *args):
        FlushCommand().do_execute(self, *args)
        return "flush"

    # Parse

    def parse(self, *args):
        if len(args[0]) == 0:
            msg = ["¿Te olvidaste el comando? Los comandos son: "]
            msg.append(self.msg_format_commands())
            raise CommandError(' - '.join(msg))
        else:
            parameters = list(args)[0]
            command = parameters.pop(0)

        try:
            return self.commands[command](*args)
        except Exception as exc:
            if type(exc) in SOCKETPY_ERRORS:
                raise ParseError(exc)
            else:
                #msg = ['Unknown command "%s"' % command]
                raise CommandError(exc)

    def msg_format_commands(self):
        comandos = self._get_commands()
        msg = ", ".join(comandos)
        return msg

    # Private Methods

    def _get_commands(self):
        comandos = list(self.commands.keys())
        comandos.sort()
        return comandos
