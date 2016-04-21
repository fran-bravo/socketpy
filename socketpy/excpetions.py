class ParseError(Exception):
    """Base socketpy exception"""


class CommandError(ParseError):
    pass


class CreateError(CommandError):
    pass


class FileError(CreateError):
    pass