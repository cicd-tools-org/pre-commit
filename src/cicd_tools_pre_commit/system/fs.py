"""Filesystem utilities for CICD tools."""

from __future__ import annotations

import os
import shutil


def rmtree(path: str) -> None:
    """Remove a directory and its contents if it exists."""
    if os.path.exists(path):
        shutil.rmtree(path)
