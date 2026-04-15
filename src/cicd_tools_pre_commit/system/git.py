"""Git utilities for CICD tools."""

from __future__ import annotations

import subprocess


def git_ls_untracked(path: str) -> list[str]:
    """List untracked files in the specified path."""
    process = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", path],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return process.stdout.decode("utf-8").splitlines()
