"""Custom argparse types for path and directory validation."""

from __future__ import annotations

import argparse
import os


def existing_directory(path: str) -> str:
    """Check if the provided path is an existing directory."""
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            f"The directory '{path}' does not exist."
        )
    return path


def valid_path(path: str) -> str:
    """Check if the provided path's parent directory exists."""
    parent = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(parent):
        raise argparse.ArgumentTypeError(
            f"The parent directory of '{path}' does not exist."
        )
    return path


def language_code(code: str) -> str:
    """Check if the language code is exactly 2 characters long."""
    if len(code) != 2:
        raise argparse.ArgumentTypeError(
            f"Language code '{code}' must be exactly 2 characters long."
        )
    return code
