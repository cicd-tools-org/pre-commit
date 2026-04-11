import argparse
import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.cli.types import file_existing


class TestFileExisting(unittest.TestCase):

    @patch("os.path.isfile")
    def test_file_existing__exists__returns_path(self, mock_isfile):
        mock_isfile.return_value = True
        path = "existing_file.txt"

        result = file_existing(path)

        self.assertEqual(result, path)
        mock_isfile.assert_called_once_with(path)

    @patch("os.path.isfile")
    def test_file_existing__not_exists__raises_argument_type_error(
        self,
        mock_isfile,
    ):
        mock_isfile.return_value = False
        path = "non_existent_file.txt"

        with self.assertRaises(argparse.ArgumentTypeError) as cm:
            file_existing(path)

        self.assertEqual(
            str(cm.exception),
            f"The file '{path}' does not exist.",
        )
        mock_isfile.assert_called_once_with(path)
