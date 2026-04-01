"""Tests for the sphinx module."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.sphinx import sphinx_build_language


class TestSphinx(unittest.TestCase):
    """Test the sphinx_build_language function."""

    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("sys.argv")
    def test_sphinx_build_language_success(
        self, mock_argv, mock_exists, mock_isdir, mock_call
    ):
        """Test successful execution of sphinx_build_language."""
        mock_argv.__getitem__.side_effect = (
            lambda s: [
                "sphinx_build_language",
                "-l",
                "EN",
                "-t",
                "source",
                "-b",
                "build",
            ][s]
        )
        mock_argv.__len__.return_value = 7
        mock_argv.__iter__.return_value = iter(
            ["sphinx_build_language", "-l", "EN", "-t", "source", "-b", "build"]
        )

        # Patch sys.argv directly instead of mocking it like above which
        # is complex
        with patch(
            "sys.argv",
            [
                "sphinx_build_language",
                "-l",
                "EN",
                "-t",
                "source",
                "-b",
                "build",
            ],
        ):
            mock_isdir.return_value = True
            mock_exists.return_value = True

            sphinx_build_language()

            mock_call.assert_called_once_with(
                [
                    "poetry",
                    "run",
                    "sphinx-build",
                    "-Ea",
                    "-b",
                    "html",
                    "-D",
                    "language=EN",
                    "source",
                    "build/EN",
                ]
            )

    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("argparse.ArgumentParser.error")
    @patch("os.path.isdir")
    @patch("os.path.exists")
    def test_sphinx_build_language_invalid_language(
        self, mock_exists, mock_isdir, mock_error, mock_call
    ):
        """Test sphinx_build_language with invalid language."""
        mock_error.side_effect = SystemExit(2)
        with patch(
            "sys.argv",
            [
                "sphinx_build_language",
                "-l",
                "ENG",
                "-t",
                "source",
                "-b",
                "build",
            ],
        ):
            with self.assertRaises(SystemExit):
                sphinx_build_language()
            mock_error.assert_called_once()
            self.assertIn(
                "must be a 2 character string", mock_error.call_args[0][0]
            )
            mock_call.assert_not_called()

    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("argparse.ArgumentParser.error")
    @patch("os.path.isdir")
    @patch("os.path.exists")
    def test_sphinx_build_language_invalid_source(
        self, mock_exists, mock_isdir, mock_error, mock_call
    ):
        """Test sphinx_build_language with invalid source."""
        mock_error.side_effect = SystemExit(2)
        with patch(
            "sys.argv",
            [
                "sphinx_build_language",
                "-l",
                "EN",
                "-t",
                "nonexistent",
                "-b",
                "build",
            ],
        ):
            mock_isdir.return_value = False
            with self.assertRaises(SystemExit):
                sphinx_build_language()
            mock_error.assert_called_once()
            self.assertIn(
                "Source folder 'nonexistent' does not exist",
                mock_error.call_args[0][0],
            )
            mock_call.assert_not_called()

    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("argparse.ArgumentParser.error")
    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.path.abspath")
    def test_sphinx_build_language_invalid_build(
        self, mock_abspath, mock_exists, mock_isdir, mock_error, mock_call
    ):
        """Test sphinx_build_language with invalid build path."""
        mock_error.side_effect = SystemExit(2)
        with patch(
            "sys.argv",
            [
                "sphinx_build_language",
                "-l",
                "EN",
                "-t",
                "source",
                "-b",
                "/invalid/path/build",
            ],
        ):
            mock_isdir.return_value = True
            mock_abspath.side_effect = lambda x: x
            mock_exists.return_value = False  # For the parent dir

            with self.assertRaises(SystemExit):
                sphinx_build_language()
            mock_error.assert_called_once()
            self.assertIn(
                "Build folder path '/invalid/path/build' is not valid",
                mock_error.call_args[0][0],
            )
            mock_call.assert_not_called()
