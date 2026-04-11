"""regex argparse type."""

import argparse
import re


def regex(pattern: str) -> str:
    """Check if the given string is a valid regex pattern."""
    try:
        re.compile(pattern)
    except re.error:
        raise argparse.ArgumentTypeError(
            f"Regex pattern '{pattern}' is invalid. ")
    return pattern
