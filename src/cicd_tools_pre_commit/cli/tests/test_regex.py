import argparse
import unittest

from cicd_tools_pre_commit.cli.types import regex


class TestRegex(unittest.TestCase):

    def test_regex__valid_short__returns_pattern(self):
        self.assertEqual(regex("input"), "input")

    def test_regex__invalid_pattern__raises_error(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            regex("+")
