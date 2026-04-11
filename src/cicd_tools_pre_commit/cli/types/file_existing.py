"""file_existing argparse type."""

import argparse
import os


def file_existing(path: str) -> str:
    """Check if the provided path is an existing file."""
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(
            f"The file '{path}' does not exist.", )
    return path
