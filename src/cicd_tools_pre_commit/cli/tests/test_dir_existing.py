import argparse
import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.cli.types import dir_existing


class TestDirExisting(unittest.TestCase):

    @patch("os.path.isdir")
    def test_path_existing__valid_dir__returns_path(
        self,
        mock_isdir,
    ):
        mock_isdir.return_value = True
        path = "/valid/dir"
        self.assertEqual(dir_existing(path), path)

    @patch("os.path.isdir")
    def test_path_existing__invalid_dir__raises_error(
        self,
        mock_isdir,
    ):
        mock_isdir.return_value = False
        with self.assertRaises(argparse.ArgumentTypeError):
            dir_existing("/invalid/dir")
