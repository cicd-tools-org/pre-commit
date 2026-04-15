import unittest
from unittest.mock import Mock, patch

from cicd_tools_pre_commit.system.git import git_ls_untracked


class TestGitLsUntracked(unittest.TestCase):

    @patch("subprocess.run")
    def test_git_ls_untracked__no_untracked_files__returns_empty_list(
        self,
        mock_run,
    ):
        mock_process = Mock()
        mock_process.stdout = b""
        mock_run.return_value = mock_process

        result = git_ls_untracked("some/path")

        self.assertEqual(result, [])
        mock_run.assert_called_once_with(
            [
                "git", "ls-files", "--others", "--exclude-standard", "--",
                "some/path",
            ],
            check=True,
            stdout=-1,
            stderr=-2,
        )

    @patch("subprocess.run")
    def test_git_ls_untracked__with_untracked_files__returns_list(
        self,
        mock_run,
    ):
        mock_process = Mock()
        mock_process.stdout = b"file1.po\nfile2.po\n"
        mock_run.return_value = mock_process

        result = git_ls_untracked("some/path")

        self.assertEqual(result, ["file1.po", "file2.po"])
