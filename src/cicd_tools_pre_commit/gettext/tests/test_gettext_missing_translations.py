import unittest
from unittest.mock import mock_open, patch

from cicd_tools_pre_commit.gettext.missing_translations import (
    gettext_translations_missing_hook,
    missing_translations,
)


class TestGettextMissingTranslations(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open,
           read_data='msgid "Hello"\nmsgstr ""\n')
    def test_missing_translations__empty_msgstr__returns_msgid(
        self, _mock_file,
    ):
        result = missing_translations("test.po")
        self.assertEqual(result, ['msgid "Hello"'])

    @patch("builtins.open", new_callable=mock_open,
           read_data='msgid "Hello"\nmsgstr "Bonjour"\n')
    def test_missing_translations__filled_msgstr__returns_empty_list(
        self, _mock_file,
    ):
        result = missing_translations("test.po")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open,
           read_data='msgid ""\nmsgstr ""\n"Content-Type: ...\\n"\n')
    def test_missing_translations__header_ignored__returns_empty_list(
        self, _mock_file,
    ):
        result = missing_translations("test.po")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open,
           read_data='msgid ""\n"First line "\n"Second line"\nmsgstr ""\n')
    def test_missing_translations__multi_line_msgid__returns_full_msgid(
        self, _mock_file,
    ):
        result = missing_translations("test.po")
        self.assertEqual(
            result, ['msgid "" "First line " "Second line"']
        )

    @patch("builtins.open", new_callable=mock_open,
           read_data='msgid "Hello"\nmsgstr ""\n"Bonjour"\n')
    def test_missing_translations__multi_line_msgstr__returns_empty_list(
        self, _mock_file,
    ):
        result = missing_translations("test.po")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open,
           read_data='# comment\nmsgid "Hello"\n# comment\nmsgstr ""\n')
    def test_missing_translations__comments_ignored__returns_msgid(
        self, _mock_file,
    ):
        result = missing_translations("test.po")
        self.assertEqual(result, ['msgid "Hello"'])

    @patch("sys.argv", ["gettext_translations_missing", "file1.po"])
    @patch("cicd_tools_pre_commit.gettext.missing_translations.file_existing")
    @patch("cicd_tools_pre_commit.gettext.missing_translations.missing_translations")
    @patch("sys.exit")
    def test_gettext_translations_missing_hook__missing_found__calls_exit(
        self,
        mock_exit,
        mock_missing,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x
        mock_missing.return_value = ['msgid "Missing"']
        gettext_translations_missing_hook()
        mock_exit.assert_called_with(1)

    @patch("sys.argv", ["gettext_translations_missing", "file1.po"])
    @patch("cicd_tools_pre_commit.gettext.missing_translations.file_existing")
    @patch("cicd_tools_pre_commit.gettext.missing_translations.missing_translations")
    @patch("sys.exit")
    def test_gettext_translations_missing_hook__no_missing__does_not_call_exit(
        self,
        mock_exit,
        mock_missing,
        mock_file_existing,
    ):
        mock_file_existing.side_effect = lambda x: x
        mock_missing.return_value = []
        gettext_translations_missing_hook()
        mock_exit.assert_not_called()
