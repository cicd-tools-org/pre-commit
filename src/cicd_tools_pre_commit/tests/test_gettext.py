import os
import tempfile
import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.gettext import (
    missing_translations,
    missing_translations_hook,
)


class TestGettext(unittest.TestCase):

    def test_missing_translations__empty_msgstr__returns_msgid(self):
        content = """
msgid "Hello"
msgstr ""
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".po", delete=False
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = missing_translations(temp_path)
            self.assertEqual(result, ['msgid "Hello"'])
        finally:
            os.remove(temp_path)

    def test_missing_translations__filled_msgstr__returns_empty_list(self):
        content = """
msgid "Hello"
msgstr "Bonjour"
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".po", delete=False
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = missing_translations(temp_path)
            self.assertEqual(result, [])
        finally:
            os.remove(temp_path)

    def test_missing_translations__header_ignored__returns_empty_list(self):
        content = """
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".po", delete=False
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = missing_translations(temp_path)
            self.assertEqual(result, [])
        finally:
            os.remove(temp_path)

    def test_missing_translations__multi_line_msgid__returns_full_msgid(self):
        content = """
msgid ""
"First line "
"Second line"
msgstr ""
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".po", delete=False
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = missing_translations(temp_path)
            self.assertEqual(
                result, ['msgid "" "First line " "Second line"']
            )
        finally:
            os.remove(temp_path)

    def test_missing_translations__multi_line_msgstr__returns_empty_list(self):
        content = """
msgid "Hello"
msgstr ""
"Bonjour"
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".po", delete=False
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = missing_translations(temp_path)
            self.assertEqual(result, [])
        finally:
            os.remove(temp_path)

    def test_missing_translations__comments_ignored__returns_msgid(self):
        content = """
# This is a comment
msgid "Hello"
# Another comment
msgstr ""
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".po", delete=False
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = missing_translations(temp_path)
            self.assertEqual(result, ['msgid "Hello"'])
        finally:
            os.remove(temp_path)

    @patch("sys.argv", ["missing_translations", "file1.po"])
    @patch("cicd_tools_pre_commit.gettext.file_existing")
    @patch("cicd_tools_pre_commit.gettext.missing_translations")
    @patch("sys.exit")
    def test_missing_translations_hook__missing_found__calls_exit(
        self,
        mock_exit,
        mock_missing,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x
        mock_missing.return_value = ['msgid "Missing"']
        missing_translations_hook()
        mock_exit.assert_called_with(1)

    @patch("sys.argv", ["missing_translations", "file1.po"])
    @patch("cicd_tools_pre_commit.gettext.file_existing")
    @patch("cicd_tools_pre_commit.gettext.missing_translations")
    @patch("sys.exit")
    def test_missing_translations_hook__no_missing__does_not_call_exit(
        self,
        mock_exit,
        mock_missing,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x
        mock_missing.return_value = []
        missing_translations_hook()
        mock_exit.assert_not_called()
