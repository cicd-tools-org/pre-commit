from __future__ import annotations

import argparse
import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.cli.types import (
    existing_directory,
    language_code,
    valid_path,
)


class TestArgparseTypes(unittest.TestCase):

    @patch("os.path.isdir")
    def test_existing_directory_success(self, mock_isdir):
        mock_isdir.return_value = True
        path = "/valid/dir"
        self.assertEqual(existing_directory(path), path)

    @patch("os.path.isdir")
    def test_existing_directory_failure(self, mock_isdir):
        mock_isdir.return_value = False
        with self.assertRaises(argparse.ArgumentTypeError):
            existing_directory("/invalid/dir")

    @patch("os.path.exists")
    @patch("os.path.abspath")
    @patch("os.path.dirname")
    def test_valid_path_success(self, mock_dirname, mock_abspath, mock_exists):
        mock_abspath.return_value = "/valid/parent/file"
        mock_dirname.return_value = "/valid/parent"
        mock_exists.return_value = True
        path = "file"
        self.assertEqual(valid_path(path), path)

    @patch("os.path.exists")
    @patch("os.path.abspath")
    @patch("os.path.dirname")
    def test_valid_path_failure(self, mock_dirname, mock_abspath, mock_exists):
        mock_abspath.return_value = "/invalid/parent/file"
        mock_dirname.return_value = "/invalid/parent"
        mock_exists.return_value = False
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_path("file")

    def test_language_code_success(self):
        self.assertEqual(language_code("EN"), "EN")
        self.assertEqual(language_code("fr"), "fr")

    def test_language_code_failure(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            language_code("ENG")
        with self.assertRaises(argparse.ArgumentTypeError):
            language_code("E")
        with self.assertRaises(argparse.ArgumentTypeError):
            language_code("")
