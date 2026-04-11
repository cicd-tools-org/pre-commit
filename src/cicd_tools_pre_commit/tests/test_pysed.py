import unittest
from unittest.mock import MagicMock, mock_open, patch

from cicd_tools_pre_commit.pysed import pysed


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
    @patch("builtins.open", new_callable=mock_open, read_data="foo content")
    def test_pysed__basic_replacement(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        pysed()

        mock_file.assert_any_call("file1.txt", "r", encoding="utf-8")
        mock_file.assert_any_call("file1.txt", "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called_once_with("bar content")

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
    def test_pysed__case_insensitive_replacement(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        pysed()

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
    def test_pysed__no_match__no_write(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        pysed()

        # Should only be opened for reading
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
    def test_pysed__multiple_files(
        self,
        mock_file,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x

        pysed()

        self.assertEqual(mock_file.call_count, 4)
        # Actually, let's just check if it was called for both files
        mock_file.assert_any_call("file1.txt", "r", encoding="utf-8")
        mock_file.assert_any_call("file1.txt", "w", encoding="utf-8")
        mock_file.assert_any_call("file2.txt", "r", encoding="utf-8")
        mock_file.assert_any_call("file2.txt", "w", encoding="utf-8")
