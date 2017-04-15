import pytest, sys, io, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from unittest import TestCase
from socketpy.filing import Filer, FileLineWrapper
from socketpy.formatter import ModelFormatter
from socketpy.parser import Parser
from socketpy.exceptions import ArgumentError


class TestFiling(TestCase):
    parser = Parser()

    def setUp(self):
        self.parser.parse(["config"])
        self.parser.parse(["create", "socket"])

    def tearDown(self):
        self.parser.parse(["delete"])
        self.parser.parse(["deconfig"])

    def test_readline(self):
        filer = Filer()
        formatter = ModelFormatter()
        path = os.path.join(os.path.join(filer.working_directory, "sockets"), formatter.file)
        fd = FileLineWrapper(open(path, "r"))
        try:
            line = fd.readline()
            assert fd.line == 1
            assert line == "#ifndef MODELOS_H_\n"
        finally:
            fd.close()

    def test_split_selector(self):
        with pytest.raises(ArgumentError):
            filer = Filer()
            filer._split_selector("dni:int:8")

