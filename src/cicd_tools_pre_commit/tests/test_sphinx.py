import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.sphinx import sphinx_build_language


class TestSphinx(unittest.TestCase):

    @patch(
        "sys.argv",
        ["sphinx_build_language", "-l", "en", "-t", "source", "-b", "build"],
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.valid_path")
    def test_sphinx_build_language__valid_args__calls_sphinx_build(
        self,
        mock_valid_path,
        mock_language_code,
        mock_existing_directory,
        mock_call,
    ):
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
                "language=en",
                "source",
                "build/en",
            ],
        )

    @patch(
        "sys.argv",
        [
            "sphinx_build_language",
            "-l",
            "invalid",
            "-t",
            "source",
            "-b",
            "build",
        ],
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("argparse.ArgumentParser.error")
    @patch("cicd_tools_pre_commit.sphinx.existing_directory")
    @patch("cicd_tools_pre_commit.sphinx.valid_path")
    def test_sphinx_build_language__invalid_language__raises_system_exit(
        self,
        mock_valid_path,
        mock_existing_directory,
        mock_error,
        mock_call,
    ):
        mock_error.side_effect = SystemExit(2)
        mock_existing_directory.side_effect = lambda x: x
        mock_valid_path.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            sphinx_build_language()

        mock_call.assert_not_called()

    @patch(
        "sys.argv",
        ["sphinx_build_language", "-l", "en", "-t", "missing", "-b", "build"],
    )
    @patch("cicd_tools_pre_commit.sphinx.call")
    @patch("argparse.ArgumentParser.error")
    @patch("cicd_tools_pre_commit.sphinx.language_code")
    @patch("cicd_tools_pre_commit.sphinx.valid_path")
    @patch("os.path.isdir")
    def test_sphinx_build_language__missing_source__raises_system_exit(
        self,
        mock_isdir,
        mock_valid_path,
        mock_language_code,
        mock_error,
        mock_call,
    ):
        mock_error.side_effect = SystemExit(2)
        mock_isdir.return_value = False
        mock_language_code.side_effect = lambda x: x
        mock_valid_path.side_effect = lambda x: x

        with self.assertRaises(SystemExit):
            sphinx_build_language()

        mock_call.assert_not_called()
