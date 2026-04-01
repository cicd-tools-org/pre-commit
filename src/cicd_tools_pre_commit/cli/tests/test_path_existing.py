import argparse
import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.cli.types import path_existing


class TestPathExisting(unittest.TestCase):

    @patch("os.path.isdir")
    def test_path_existing__valid_dir__returns_path(
        self,
        mock_isdir,
    ):
        mock_isdir.return_value = True
        path = "/valid/dir"
        self.assertEqual(path_existing(path), path)

    @patch("os.path.isdir")
    def test_path_existing__invalid_dir__raises_error(
        self,
        mock_isdir,
    ):
        mock_isdir.return_value = False
        with self.assertRaises(argparse.ArgumentTypeError):
            path_existing("/invalid/dir")
