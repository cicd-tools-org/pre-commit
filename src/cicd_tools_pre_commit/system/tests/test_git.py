import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.system.git import git_ls_untracked


class TestGitLsUntracked(unittest.TestCase):

    @patch("cicd_tools_pre_commit.system.git.call")
    def test_git_ls_untracked__no_untracked_files__returns_empty_list(
        self,
        mock_call,
    ):
        mock_call.return_value = ""

        result = git_ls_untracked("some/path")

        self.assertEqual(result, [])
        mock_call.assert_called_once_with(
            [
                "git", "ls-files", "--others", "--exclude-standard", "--",
                "some/path",
            ],
            capture_output=True,
        )

    @patch("cicd_tools_pre_commit.system.git.call")
    def test_git_ls_untracked__with_untracked_files__returns_list(
        self,
        mock_call,
    ):
        mock_call.return_value = "file1.po\nfile2.po\n"

        result = git_ls_untracked("some/path")

        self.assertEqual(result, ["file1.po", "file2.po"])
