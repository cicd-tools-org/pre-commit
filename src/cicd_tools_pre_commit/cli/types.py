"""Custom argparse types for CLI argument validation."""

import argparse
import os
import re

LANGUAGE_CODE_REGEX = re.compile(r"^[a-z]{2}(_[A-Z]{2})?$")


def existing_directory(path: str) -> str:
    """Check if the provided path is an existing directory."""
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            f"The directory '{path}' does not exist.",
        )
    return path


def valid_path(path: str) -> str:
    """Check if the provided path's parent directory exists."""
    parent = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(parent):
        raise argparse.ArgumentTypeError(
            f"The parent directory of '{path}' does not exist.",
        )
    return path


def language_code(code: str) -> str:
    """Check if the language code matches the allowed pattern."""
    if not LANGUAGE_CODE_REGEX.match(code):
        raise argparse.ArgumentTypeError(
            f"Language code '{code}' is invalid. "
            "Expected format like 'en' or 'zh_CN'.",
        )
    return code
