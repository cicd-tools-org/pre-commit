"""Test the system call function."""

import io
import shlex
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from cicd_tools_pre_commit.system import CALL_ERROR, call


class TestCall(unittest.TestCase):

    def setUp(self) -> None:
        self.stdout_capture = io.StringIO()
        self.stderr_capture = io.StringIO()

    def test_call__no_error__outputs_stdout_and_stderr(self) -> None:
        with (redirect_stdout(self.stdout_capture),
              redirect_stderr(self.stderr_capture)):
            result = call(shlex.split("bash -c 'echo stdout; echo stderr >&2'"))

        assert self.stdout_capture.getvalue() == "stdout\nstderr\n"
        assert self.stderr_capture.getvalue() == ""
        assert result == "stdout\nstderr\n"

    @mock.patch("sys.exit")
    def test_call__no_error__returns_correct_exit_code(
        self,
        mocked_exit,
    ) -> None:
        with (redirect_stdout(self.stdout_capture),
              redirect_stderr(self.stderr_capture)):
            call(shlex.split("bash -c 'echo stdout; echo stderr >&2'"))

        mocked_exit.assert_not_called()

    @mock.patch("sys.exit", mock.Mock())
    def test_call__with_error__outputs_stdout_and_stderr(self) -> None:
        with (redirect_stdout(self.stdout_capture),
              redirect_stderr(self.stderr_capture)):
            result = call(
                shlex.split(
                    "bash -c 'echo stdout; echo stderr >&2; exit 127'"))

        assert self.stdout_capture.getvalue() == (
            f"stdout\nstderr\n{CALL_ERROR.format(127)}\n")
        assert self.stderr_capture.getvalue() == ""
        assert result == "stdout\nstderr\n"

    @mock.patch("sys.exit")
    def test_call__with_error__returns_correct_exit_code(
        self,
        mocked_exit,
    ) -> None:
        with (redirect_stdout(self.stdout_capture),
              redirect_stderr(self.stderr_capture)):
            call(shlex.split("bash -c 'exit 127'"))

        mocked_exit.assert_called_once_with(127)

    def test_call__print_output_false__no_print(self) -> None:
        with (redirect_stdout(self.stdout_capture),
              redirect_stderr(self.stderr_capture)):
            result = call(
                shlex.split("echo 'test output'"),
                print_output=False,
            )

        assert self.stdout_capture.getvalue() == ""
        assert result == "test output\n"

    @mock.patch("sys.exit")
    def test_call__print_output_false__error__prints_and_exits(
        self,
        mocked_exit,
    ) -> None:
        with (redirect_stdout(self.stdout_capture),
              redirect_stderr(self.stderr_capture)):
            result = call(
                shlex.split("bash -c 'echo \"error output\"; exit 1'"),
                print_output=False,
            )

        assert self.stdout_capture.getvalue() == (
            f"error output\n{CALL_ERROR.format(1)}\n")
        assert result == "error output\n"
        mocked_exit.assert_called_once_with(1)
