"""Git utilities for CICD tools."""

from __future__ import annotations

from .call import call


def git_ls_untracked(path: str) -> list[str]:
    """List untracked files in the specified path."""
    output = call(
        ["git", "ls-files", "--others", "--exclude-standard", "--", path],
        print_output=False,
    )
    return [line for line in output.splitlines() if line.endswith(".po")]
