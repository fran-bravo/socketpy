from unittest import TestCase
from socketpy.analyzer import Analyzer
import pytest


class TestAnalyzer(TestCase):
    analyzer = Analyzer()

    def test_analyze_type(self):
        assert self.analyzer.analyze_type("int") == True

    def test_analyze_wrong_type(self):
        assert self.analyzer.analyze_type("Boolean") == False

    def test_analyze_ptr_type(self):
        assert self.analyzer.analyze_type("int*") == True

    def test_analyze_wrong_ptr_type(self):
        assert self.analyzer.analyze_type("Boolean*") == False

    def test_analyze_array_type(self):
        assert self.analyzer.analyze_type("int[10]") == True

    def test_analyze_wrong_array_type(self):
        assert self.analyzer.analyze_type("Boolean[32]") == False

    def test_analyze_wrong_array_not_numbers(self):
        assert self.analyzer.analyze_type("Boolean[asd]") == False