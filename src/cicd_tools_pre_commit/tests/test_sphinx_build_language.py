import argparse
import os
import unittest
from unittest.mock import Mock, patch

from cicd_tools_pre_commit.sphinx import sphinx_build_language


class TestSphinxBuildLanguage(unittest.TestCase):

    @patch(
        "sys.argv",
        [
            "sphinx_build_language",
            "-l",
            "en",
            "-s",
            "source",
            "-b",
            "build",
        ],
    )
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_build_language__valid_args__calls_sphinx_build(
        self,
        mock_call,
        mock_language_code,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_existing.side_effect = lambda x: x
        mock_language_code.side_effect = lambda x: x
        mock_dir_valid.side_effect = lambda x: x

        sphinx_build_language()

        mock_call.assert_called_once_with([
            "poetry",
            "run",
            "sphinx-build",
            "-Ea",
            "-b",
            "html",
            "-D",
            "language=en",
            "source",
            os.path.join("source", "build", "en"),
        ], )

    @patch(
        "sys.argv",
        [
            "sphinx_build_language",
            "-l",
            "en",
            "-s",
            "source",
            "-b",
            "build",
        ],
    )
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("os.environ")
    @patch("cicd_tools_pre_commit.sphinx.call", Mock())
    def test_sphinx_build_language__valid_args__clears_conflicting_virtual_envs(
        self,
        mock_os_environ,
        mock_language_code,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_existing.side_effect = lambda x: x
        mock_language_code.side_effect = lambda x: x
        mock_dir_valid.side_effect = lambda x: x

        sphinx_build_language()

        mock_os_environ.pop.assert_called_once_with("VIRTUAL_ENV", None)

    @patch(
        "sys.argv",
        [
            "sphinx_build_language",
            "-l",
            "invalid",
            "-s",
            "source",
            "-b",
            "build",
        ],
    )
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_build_language__invalid_language__raises_system_exit(
        self,
        mock_call,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_existing.side_effect = lambda x: x
        mock_dir_valid.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            sphinx_build_language()

        mock_call.assert_not_called()

    @patch(
        "sys.argv",
        [
            "sphinx_build_language",
            "-l",
            "en",
            "-s",
            "missing",
            "-b",
            "build",
        ],
    )
    @patch("cicd_tools_pre_commit.sphinx.dir_valid")
    @patch("cicd_tools_pre_commit.sphinx.dir_existing")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.call")
    def test_sphinx_build_language__missing_source__raises_system_exit(
        self,
        mock_call,
        mock_language_code,
        mock_dir_existing,
        mock_dir_valid,
    ):
        mock_dir_existing.side_effect = argparse.ArgumentError
        mock_language_code.side_effect = lambda x: x
        mock_dir_valid.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            sphinx_build_language()

        mock_call.assert_not_called()
