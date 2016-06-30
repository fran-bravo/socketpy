class ParseError(Exception):
    """Base socketpy exception"""


class CommandError(ParseError):
    pass


class CreateError(CommandError):
    pass


class HelpError(CommandError):
    pass


class FileError(CreateError):
    pass


class RouteError(CommandError):
    pass


class FlushError(CommandError):
    pass


class EmbedError(CommandError):
    pass


SOCKETPY_ERRORS = [ParseError, HelpError, CommandError, CreateError, RouteError, FileError, FlushError, EmbedError]
