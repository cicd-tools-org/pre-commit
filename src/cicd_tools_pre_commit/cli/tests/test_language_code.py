import argparse
import unittest

from cicd_tools_pre_commit.cli.types import language_code


class TestLanguageCode(unittest.TestCase):

    def test_language_code__valid_short__returns_code(self):
        self.assertEqual(language_code("en"), "en")

    def test_language_code__valid_long__returns_code(self):
        self.assertEqual(language_code("zh_CN"), "zh_CN")

    def test_language_code__invalid_format__raises_error(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            language_code("ENG")

    def test_language_code__uppercase_short__raises_error(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            language_code("EN")

    def test_language_code__hyphenated__raises_error(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            language_code("en-US")

    def test_language_code__empty__raises_error(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            language_code("")
