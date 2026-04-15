"""Interface CICD-Tools with the underlying system."""

from __future__ import annotations

import subprocess
import sys

from .fs import rmtree as rmtree
from .git import git_ls_untracked as git_ls_untracked

CALL_ERROR = "ERROR: non-zero exit status ({})"


def call(command: list[str], cwd: str | None = None) -> None:
    """Execute the specified system call."""
    try:
        process = subprocess.run(
            command,
            check=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(f"{process.stdout.decode('utf-8')}", end="")
    except subprocess.CalledProcessError as exc:
        print(f"{exc.stdout.decode('utf-8')}", end="")
        print(CALL_ERROR.format(exc.returncode))
        sys.exit(exc.returncode)
