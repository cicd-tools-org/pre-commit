import unittest
from unittest.mock import patch

from cicd_tools_pre_commit.system.fs import rmtree


class TestFs(unittest.TestCase):

    @patch("os.path.exists")
    @patch("shutil.rmtree")
    def test_rmtree__path_exists__calls_shutil_rmtree(
        self,
        mock_shutil_rmtree,
        mock_path_exists,
    ):
        mock_path_exists.return_value = True

        rmtree("some/path")

        mock_shutil_rmtree.assert_called_once_with("some/path")

    @patch("os.path.exists")
    @patch("shutil.rmtree")
    def test_rmtree__path_does_not_exist__does_not_call_shutil_rmtree(
        self,
        mock_shutil_rmtree,
        mock_path_exists,
    ):
        mock_path_exists.return_value = False

        rmtree("some/path")

        mock_shutil_rmtree.assert_not_called()
