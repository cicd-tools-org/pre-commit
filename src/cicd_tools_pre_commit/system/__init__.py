"""Interface CICD-Tools with the underlying system."""

from __future__ import annotations

import subprocess
import sys

CALL_ERROR = "ERROR: non-zero exit status ({})"


def call(
    command: list[str],
    cwd: str | None = None,
    mute: bool = False,
) -> str:
    """Execute the specified system call."""
    try:
        process = subprocess.run(
            command,
            check=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = process.stdout.decode("utf-8")
        if not mute:
            print(f"{output}", end="")
    except subprocess.CalledProcessError as exc:
        output = exc.stdout.decode("utf-8")
        print(f"{output}", end="")
        print(CALL_ERROR.format(exc.returncode))
        sys.exit(exc.returncode)

    return output
