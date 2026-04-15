import argparse
import os
import unittest
from unittest.mock import Mock, call, patch

from cicd_tools_pre_commit.sphinx import (
    SPHINX_DEFAULT_GETTEXT_FOLDER,
    SPHINX_DEFAULT_LOCALES_FOLDER,
    sphinx_translate,
)


class TestSphinxTranslate(unittest.TestCase):

    call_with_default_folders = patch("sys.argv", [
        "sphinx_translate",
        "-b",
        "build_folder",
        "-s",
        "documentation_folder",
    ])
    call_with_specified_folders = patch("sys.argv", [
        "sphinx_translate",
        "-b",
        "build_folder",
        "-l",
        "custom_locales",
        "-g",
        "custom_gettext",
        "-s",
        "documentation_folder",
    ])

    @call_with_default_folders
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.rmtree", Mock())
    @patch(
        "cicd_tools_pre_commit.sphinx.git_ls_untracked",
        Mock(return_value=[]),
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_translate__valid_args__default_folders__calls_commands(
        self,
        mock_call,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = lambda x: x
        mock_dir_existing.side_effect = lambda x: x

        sphinx_translate()

        expected_calls = [
            call([
                "poetry",
                "run",
                "sphinx-build",
                "-b",
                "gettext",
                "documentation_folder",
                os.path.join("build_folder", SPHINX_DEFAULT_GETTEXT_FOLDER),
            ]),
            call([
                "poetry",
                "run",
                "sphinx-intl",
                "update",
                "-p",
                os.path.join("build_folder", SPHINX_DEFAULT_GETTEXT_FOLDER),
                "-d",
                os.path.join("documentation_folder",
                             SPHINX_DEFAULT_LOCALES_FOLDER),
            ]),
        ]
        mock_call.assert_has_calls(expected_calls)

    @call_with_specified_folders
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.rmtree", Mock())
    @patch(
        "cicd_tools_pre_commit.sphinx.git_ls_untracked",
        Mock(return_value=[]),
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_translate__valid_args__specified_folders__calls_commands(
        self,
        mock_call,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = lambda x: x
        mock_dir_existing.side_effect = lambda x: x

        sphinx_translate()

        expected_calls = [
            call([
                "poetry",
                "run",
                "sphinx-build",
                "-b",
                "gettext",
                "documentation_folder",
                os.path.join("build_folder", "custom_gettext"),
            ]),
            call([
                "poetry",
                "run",
                "sphinx-intl",
                "update",
                "-p",
                os.path.join("build_folder", "custom_gettext"),
                "-d",
                os.path.join("documentation_folder", "custom_locales"),
            ]),
        ]
        mock_call.assert_has_calls(expected_calls)

    @call_with_default_folders
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("os.environ")
    @patch("cicd_tools_pre_commit.sphinx.rmtree", Mock())
    @patch(
        "cicd_tools_pre_commit.sphinx.git_ls_untracked",
        Mock(return_value=[]),
    )
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

    @call_with_default_folders
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.rmtree")
    @patch(
        "cicd_tools_pre_commit.sphinx.git_ls_untracked",
        Mock(return_value=[]),
    )
    @patch("cicd_tools_pre_commit.sphinx.call", Mock())
    def test_sphinx_translate__valid_args__removes_gettext_folder(
        self,
        mock_rmtree,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = lambda x: x
        mock_dir_existing.side_effect = lambda x: x

        sphinx_translate()

        mock_rmtree.assert_called_once_with(
            os.path.join("build_folder", SPHINX_DEFAULT_GETTEXT_FOLDER))

    @call_with_default_folders
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.rmtree", Mock())
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

    @call_with_default_folders
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.rmtree", Mock())
    @patch("cicd_tools_pre_commit.sphinx.git_ls_untracked")
    @patch("cicd_tools_pre_commit.sphinx.call", Mock())
    def test_sphinx_translate__untracked_files_found__exits_with_error(
        self,
        mock_git_ls_untracked,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_valid.side_effect = lambda x: x
        mock_dir_existing.side_effect = lambda x: x
        mock_git_ls_untracked.return_value = ["new_file.po"]

        with self.assertRaises(SystemExit) as cm:
            sphinx_translate()

        self.assertEqual(cm.exception.code, 1)

    @call_with_default_folders
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.rmtree", Mock())
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
