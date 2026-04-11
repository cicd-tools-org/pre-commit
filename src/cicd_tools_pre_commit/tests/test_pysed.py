import argparse
import unittest
from unittest.mock import mock_open, patch

from cicd_tools_pre_commit import pysed


class TestPysed(unittest.TestCase):

    @patch(
        "sys.argv",
        [
            "pysed",
            "-p",
            "foo",
            "-r",
            "bar",
            "file1.txt",
        ],
    )
    @patch("cicd_tools_pre_commit.pysed.file_existing")
    @patch("cicd_tools_pre_commit.pysed.regex")
    def test_pysed__invalid_regex__raises_exception(
        self,
        mock_file_existing,
        mock_regex,
    ):
        mock_file_existing.side_effect = lambda x: x
        mock_regex.side_effect = argparse.ArgumentError

        with self.assertRaises(SystemExit):
            pysed.pysed_hook()

    @patch(
        "sys.argv",
        [
            "pysed",
            "-p",
            "foo",
            "-r",
            "bar",
            "file1.txt",
        ],
    )
    @patch("cicd_tools_pre_commit.pysed.file_existing")
    @patch("builtins.open", new_callable=mock_open, read_data="foo content")
    def test_pysed__basic_replacement__writes_correct_content(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            pysed.pysed_hook()

        mock_file.assert_any_call("file1.txt", "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called_once_with("bar content")

    @patch(
        "sys.argv",
        [
            "pysed",
            "-p",
            "foo",
            "-r",
            "bar",
            "file1.txt",
        ],
    )
    @patch("cicd_tools_pre_commit.pysed.file_existing")
    @patch("builtins.open", new_callable=mock_open, read_data="foo content")
    def test_pysed__basic_replacement__exits_with_one(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        with self.assertRaises(SystemExit) as cm:
            pysed.pysed_hook()

        self.assertEqual(cm.exception.code, 1)

    @patch(
        "sys.argv",
        [
            "pysed",
            "-p",
            "FOO",
            "-r",
            "bar",
            "-i",
            "file1.txt",
        ],
    )
    @patch("cicd_tools_pre_commit.pysed.file_existing")
    @patch("builtins.open", new_callable=mock_open, read_data="foo content")
    def test_pysed__case_insensitive_flag__performs_replacement(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            pysed.pysed_hook()

        handle = mock_file()
        handle.write.assert_called_once_with("bar content")

    @patch(
        "sys.argv",
        [
            "pysed",
            "-p",
            "foo",
            "-r",
            "bar",
            "file1.txt",
        ],
    )
    @patch("cicd_tools_pre_commit.pysed.file_existing")
    @patch("builtins.open", new_callable=mock_open, read_data="no match")
    def test_pysed__no_match__does_not_write_to_file(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        pysed.pysed_hook()

        mock_file.assert_called_once_with("file1.txt", "r", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_not_called()

    @patch(
        "sys.argv",
        [
            "pysed",
            "-p",
            "foo",
            "-r",
            "bar",
            "file1.txt",
            "file2.txt",
        ],
    )
    @patch("cicd_tools_pre_commit.pysed.file_existing")
    @patch("builtins.open", new_callable=mock_open, read_data="foo")
    def test_pysed__multiple_files__processes_all_files(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            pysed.pysed_hook()

        mock_file.assert_any_call("file1.txt", "r", encoding="utf-8")
        mock_file.assert_any_call("file1.txt", "w", encoding="utf-8")
        mock_file.assert_any_call("file2.txt", "r", encoding="utf-8")
        mock_file.assert_any_call("file2.txt", "w", encoding="utf-8")
