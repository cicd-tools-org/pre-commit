"""Git utilities for CICD tools."""

from __future__ import annotations

from .call import call


def git_ls_untracked(path: str) -> list[str]:
    """List untracked files in the specified path."""
    output = call(
        ["git", "ls-files", "--others", "--exclude-standard", "--", path],
        capture_output=True,
    )
    if not output:
        return []

    return output.splitlines()
