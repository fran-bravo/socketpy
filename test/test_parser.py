from unittest import TestCase
from socketpy.parser import Parser, ParseError
import pytest


class TestParser(TestCase):
    parser = Parser()

    def test_parse_command_help(self):
        result = self.parser.parse(["help", "test"])
        assert result == "help"

    def test_parse_command_create(self):
        result = self.parser.parse(["create", "socket", "test"])
        assert result == "create"

    def test_parse_fail(self):
        with pytest.raises(ParseError):
            self.parser.parse(["run"])

    def test_parse_no_parameters(self):
        with pytest.raises(ParseError):
            self.parser.parse([])
