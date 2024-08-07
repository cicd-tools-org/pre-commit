"""Tests for CICD-Tools pre-commit resource exposure utility."""

import unittest
from unittest import mock

import cicd_tools_pre_commit
from cicd_tools_pre_commit import resources


class TestResourceExpose(unittest.TestCase):
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
        "sys.argv",
        arguments_not_passed,
    )
    @mock.patch(
        "cicd_tools_pre_commit.resources.call",
        mock_system,
    )
    def test__arguments_not_passed__executes_without_arguments(self) -> None:
        try:
            cicd_tools_pre_commit.with_cicd_resources()
        except Exception as exc:
            assert exc.args == (resources.INSUFFICIENT_ARGUMENTS_ERROR, )

    @mock.patch(
        "sys.argv",
        arguments_resources_not_requested,
    )
    @mock.patch(
        "cicd_tools_pre_commit.resources.call",
        mock_system,
    )
    def test__resources_not_requested__does_not_modify_args(self) -> None:
        cicd_tools_pre_commit.with_cicd_resources()

        self.mock_system.assert_called_once_with(
            self.arguments_resources_not_requested[1:])

    @mock.patch(
        "sys.argv",
        arguments_requested,
    )
    @mock.patch(
        "cicd_tools_pre_commit.resources.call",
        mock_system,
    )
    def test__resources_requested__modifies_args(self) -> None:
        cicd_tools_pre_commit.with_cicd_resources()

        self.mock_system.assert_called_once_with([
            self.arguments_requested[1].format(
                **
                {resources.RESOURCES_VARIABLE_NAME: resources.RESOURCES_PATH}),
            self.arguments_requested[2],
        ])
