"""Tests for the sphinx module."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.sphinx import sphinx_build_language


class TestSphinx(unittest.TestCase):
    """Test the sphinx_build_language function."""

    @patch(
        "sys.argv",
        ["sphinx_build_language", "-l", "EN", "-t", "source", "-b", "build"],
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.valid_path")
    def test_sphinx_build_language_success(
        self,
        mock_valid_path,
        mock_language_code,
        mock_existing_directory,
        mock_call,
    ):
        """Test successful execution of sphinx_build_language."""
        mock_existing_directory.side_effect = lambda x: x
        mock_language_code.side_effect = lambda x: x
        mock_valid_path.side_effect = lambda x: x

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
            ],
        )

    @patch(
        "sys.argv",
        ["sphinx_build_language", "-l", "ENG", "-t", "source", "-b", "build"],
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.valid_path")
    def test_sphinx_build_language_invalid_language(
        self,
        mock_valid_path,
        mock_language_code,
        mock_existing_directory,
        mock_call,
    ):
        """Test sphinx_build_language with invalid language."""
        mock_language_code.side_effect = SystemExit(2)

        with self.assertRaises(SystemExit):
            sphinx_build_language()

        mock_call.assert_not_called()

    @patch(
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
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.valid_path")
    def test_sphinx_build_language_invalid_source(
        self,
        mock_valid_path,
        mock_language_code,
        mock_existing_directory,
        mock_call,
    ):
        """Test sphinx_build_language with invalid source."""
        mock_existing_directory.side_effect = SystemExit(2)

        with self.assertRaises(SystemExit):
            sphinx_build_language()

        mock_call.assert_not_called()

    @patch(
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
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.valid_path")
    def test_sphinx_build_language_invalid_build(
        self,
        mock_valid_path,
        mock_language_code,
        mock_existing_directory,
        mock_call,
    ):
        """Test sphinx_build_language with invalid build path."""
        mock_valid_path.side_effect = SystemExit(2)

        with self.assertRaises(SystemExit):
            sphinx_build_language()

        mock_call.assert_not_called()
