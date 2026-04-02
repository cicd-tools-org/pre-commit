import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.cli.types import valid_path


class TestValidPath(unittest.TestCase):

    @patch("os.path.exists")
    @patch("os.path.abspath")
    @patch("os.path.dirname")
    def test_valid_path__parent_exists__returns_path(
        self,
        mock_dirname,
        mock_abspath,
        mock_exists,
    ):
        mock_abspath.return_value = "/valid/parent/file"
        mock_dirname.return_value = "/valid/parent"
        mock_exists.return_value = True
        path = "file"
        self.assertEqual(valid_path(path), path)

    @patch("os.path.exists")
    @patch("os.path.abspath")
    @patch("os.path.dirname")
    def test_valid_path__parent_missing__raises_error(
        self,
        mock_dirname,
        mock_abspath,
        mock_exists,
    ):
        mock_abspath.return_value = "/invalid/parent/file"
        mock_dirname.return_value = "/invalid/parent"
        mock_exists.return_value = False
        with self.assertRaises(Exception):
            valid_path("file")
