from socketpy.exceptions import CommandError, ParseError, SOCKETPY_ERRORS
from socketpy.commands import HelpCommand, CreateCommand, ConfigCommand, FlushCommand, \
                              DeleteCommand, RouteCommand, DeconfigCommand, ResetCommand, \
                              EmbedCommand, CompileCommand, DecompileCommand


class Parser:

    def __init__(self):
        self.commands = {'help': self.parser_help, 'create': self.create,
                         'config': self.config, 'flush': self.flush,
                         'delete': self.delete, 'route': self.route,
                         'deconfig': self.deconfig, 'reset': self.reset,
                         'embed': self.embed, 'compile': self.compile,
                         'decompile': self.decompile}
        self.helpers = {'help': [], 'create': ['model', 'socket'], 'config': [],
                        'flush': ['types', 'routes'], 'delete': [], 'route': [],
                        'deconfig': [], 'reset': [], 'embed': [], 'compile': [],
                        'decompile': []}

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

    def deconfig(self, *args):
        DeconfigCommand().do_execute(self, *args)
        return "deconfig"

    def reset(self, *args):
        ResetCommand().do_execute(self, *args)
        return "reset"

    def flush(self, *args):
        FlushCommand().do_execute(self, *args)
        return "flush"

    def embed(self, *args):
        EmbedCommand().do_execute(self, *args)
        return "embed"

    def compile(self, *args):
        CompileCommand().do_execute(self, *args)
        return "compile"

    def decompile(self, *args):
        DecompileCommand().do_execute(self, *args)
        return "compile"

    # Parse

    def parse(self, *args):
        """
        Parses the input from STDIN, obtains the command and calls it with the rest of the arguments
        
        :param args: Input received from STDIN 
        :return: A message of the command executed or an error
        """

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
            if type(exc) not in SOCKETPY_ERRORS:
                raise ParseError(exc)
            else:
                # msg = ['Unknown command "%s"' % command]
                raise exc

    def msg_format_commands(self):
        """
        Method that gets all the commands of the parser and formats it for a nice print
        
        :return: The commands of the parser formatted 
        """

        comandos = self._get_commands()
        msg = ", ".join(comandos)
        return msg

    # Private Methods

    def _get_commands(self):
        """
        Method that gets all the commands of the parser and sorts them
        
        :return: List of Commands sorted 
        """

        comandos = list(self.commands.keys())
        comandos.sort()
        return comandos
