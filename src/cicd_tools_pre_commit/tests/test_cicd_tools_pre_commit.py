"""Tests for CICD-Tools pre-commit resource exposure utility."""

import unittest
from unittest import mock

import cicd_tools_pre_commit


class TestResourceExpose(unittest.TestCase):
    """Tests for CICD-Tools pre-commit resource exposure utility."""

    mock_system = mock.Mock()
    arguments_not_passed = ["ProgramName"]
    arguments_resources_not_requested = ["ProgramName", "Arg1", "Arg2"]
    arguments_requested = [
        "ProgramName",
        "{CICD_RESOURCES}/schemas/cookiecutter.json",
        "Arg2",
    ]

    def setUp(self) -> None:
        self.mock_system.reset_mock()

    @mock.patch(
        cicd_tools_pre_commit.__name__ + ".sys.argv",
        arguments_not_passed,
    )
    @mock.patch(cicd_tools_pre_commit.__name__ + ".os.system", mock_system)
    def test__arguments_not_passed__executes_without_arguments(self) -> None:
        try:
            cicd_tools_pre_commit.main()
        except Exception as exc:
            assert exc.args == (
                cicd_tools_pre_commit.INSUFFICIENT_ARGUMENTS_ERROR,
            )

    @mock.patch(
        cicd_tools_pre_commit.__name__ + ".sys.argv",
        arguments_resources_not_requested,
    )
    @mock.patch(cicd_tools_pre_commit.__name__ + ".os.system", mock_system)
    def test__resources_not_requested__does_not_modify_args(self) -> None:
        cicd_tools_pre_commit.main()

        self.mock_system.assert_called_once_with(
            " ".join(self.arguments_resources_not_requested[1:])
        )

    @mock.patch(
        cicd_tools_pre_commit.__name__ + ".sys.argv", arguments_requested
    )
    @mock.patch(cicd_tools_pre_commit.__name__ + ".os.system", mock_system)
    def test__resources_requested__modifies_args(self) -> None:
        cicd_tools_pre_commit.main()

        self.mock_system.assert_called_once_with(
            " ".join(
                [
                    self.arguments_requested[1].format(
                        **{
                            cicd_tools_pre_commit.RESOURCES_VARIABLE_NAME: cicd_tools_pre_commit.RESOURCES_PATH
                        }
                    ),
                    self.arguments_requested[2],
                ]
            )
        )


if __name__ == "__main__":
    unittest.main()
