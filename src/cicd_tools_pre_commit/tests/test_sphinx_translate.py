import unittest
from unittest.mock import call, patch

from cicd_tools_pre_commit.sphinx import sphinx_translate


class TestSphinxTranslate(unittest.TestCase):

    @patch("sys.argv", ["sphinx_translate", "-d", "documentation_folder"])
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    def test_sphinx_translate__valid_args__calls_commands(
        self,
        mock_existing_directory,
        mock_call,
    ):
        mock_existing_directory.side_effect = lambda x: x

        sphinx_translate()

        expected_calls = [
            call(
                ["poetry", "run", "make", "gettext"],
                cwd="documentation_folder",
            ),
            call(
                ["poetry", "run", "sphinx-intl", "update"],
                cwd="documentation_folder",
            ),
        ]
        mock_call.assert_has_calls(expected_calls)

    @patch("sys.argv", ["sphinx_translate", "-d", "missing_folder"])
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("argparse.ArgumentParser.error")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    def test_sphinx_translate__invalid_directory__raises_system_exit(
        self,
        mock_existing_directory,
        mock_error,
        mock_call,
    ):
        mock_error.side_effect = SystemExit(2)
        mock_existing_directory.side_effect = SystemExit(2)

        with self.assertRaises(SystemExit):
            sphinx_translate()

        mock_call.assert_not_called()
