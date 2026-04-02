"""valid_path argparse type."""

import argparse
import os


def valid_path(path: str) -> str:
    """Check if the provided path's parent directory exists."""
    parent = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(parent):
        raise argparse.ArgumentTypeError(
            f"The parent directory of '{path}' does not exist.",
        )
    return path
