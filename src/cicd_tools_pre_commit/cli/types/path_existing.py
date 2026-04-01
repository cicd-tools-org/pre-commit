"""path_existing argparse type."""

import argparse
import os


def path_existing(path: str) -> str:
    """Check if the provided path is an existing directory."""
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            f"The directory '{path}' does not exist.", )
    return path
