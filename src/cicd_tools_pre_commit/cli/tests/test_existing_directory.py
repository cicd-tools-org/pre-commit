import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.cli.types import existing_directory


class TestExistingDirectory(unittest.TestCase):

    @patch("os.path.isdir")
    def test_existing_directory__valid_dir__returns_path(
        self,
        mock_isdir,
    ):
        mock_isdir.return_value = True
        path = "/valid/dir"
        self.assertEqual(existing_directory(path), path)

    @patch("os.path.isdir")
    def test_existing_directory__invalid_dir__raises_error(
        self,
        mock_isdir,
    ):
        mock_isdir.return_value = False
        with self.assertRaises(Exception):
            existing_directory("/invalid/dir")
