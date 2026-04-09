import argparse
import unittest
from unittest.mock import Mock, call, patch

from cicd_tools_pre_commit.sphinx import sphinx_translate


class TestSphinxTranslate(unittest.TestCase):

    @patch("sys.argv", [
        "sphinx_translate",
        "-b",
        "build",
        "-s",
        "documentation_folder",
    ])
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_translate__valid_args__calls_commands(
        self,
        mock_call,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = lambda x: x
        mock_dir_existing.side_effect = lambda x: x

        sphinx_translate()

        expected_calls = [
            call(
                [
                    "poetry",
                    "run",
                    "sphinx-build",
                    "-b",
                    "gettext",
                    ".",
                    "build/gettext",
                ],
                cwd="documentation_folder",
            ),
            call(
                [
                    "poetry",
                    "run",
                    "sphinx-intl",
                    "update",
                    "-p",
                    "build/gettext",
                ],
                cwd="documentation_folder",
            ),
        ]
        mock_call.assert_has_calls(expected_calls)

    @patch("sys.argv", [
        "sphinx_translate",
        "-b",
        "build",
        "-s",
        "documentation_folder",
    ])
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("os.environ")
    @patch("cicd_tools_pre_commit.sphinx.call", Mock())
    def test_sphinx_translate__valid_args__clears_conflicting_virtual_envs(
        self,
        mock_os_environ,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = lambda x: x
        mock_dir_existing.side_effect = lambda x: x

        sphinx_translate()

        mock_os_environ.pop.assert_called_once_with("VIRTUAL_ENV", None)

    @patch("sys.argv", [
        "sphinx_translate",
        "-b",
        "build",
        "-s",
        "documentation_folder",
    ])
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_translate__invalid_doc_directory__raises_system_exit(
        self,
        mock_call,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = lambda x: x
        mock_dir_existing.side_effect = argparse.ArgumentTypeError

        with self.assertRaises(SystemExit):
            sphinx_translate()

        mock_call.assert_not_called()

    @patch("sys.argv", [
        "sphinx_translate",
        "-b",
        "build",
        "-s",
        "documentation_folder",
    ])
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_translate__invalid_build_directory__raises_system_exit(
        self,
        mock_call,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = argparse.ArgumentTypeError
        mock_dir_existing.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            sphinx_translate()

        mock_call.assert_not_called()
