import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import pytest
from unittest import TestCase
from socketpy.parser import Parser, ParseError


class TestParser(TestCase):
    parser = Parser()

    def test_parse_command_help_wrong(self):
        with pytest.raises(ParseError):
            result = self.parser.parse(["help", "test"])

    def test_parse_command_help(self):
        result = self.parser.parse(["help", "help"])
        assert result == "help"

    def test_parse_command_create(self):
        self.parser.parse(["config"])
        result = self.parser.parse(["create", "socket", "test"])
        assert result == "create"
        self.parser.parse(["delete"])
        self.parser.parse(["deconfig"])

    def test_parse_fail(self):
        with pytest.raises(ParseError):
            self.parser.parse(["run"])

    def test_parse_no_parameters(self):
        with pytest.raises(ParseError):
            self.parser.parse([])
