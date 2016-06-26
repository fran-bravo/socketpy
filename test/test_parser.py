from unittest import TestCase
from socketpy.parser import Parser, ParseError
import pytest


class TestParser(TestCase):
    parser = Parser()

    def test_parse_command_help_wrong(self):
        with pytest.raises(ParseError):
            result = self.parser.parse(["help", "test"])

    def test_parse_command_help(self):
        result = self.parser.parse(["help", "help"])
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
