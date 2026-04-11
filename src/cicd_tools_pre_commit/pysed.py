"""Sed-like find and replace using Python."""

import argparse
import re
import sys
from typing import List

from .cli.types import file_existing


def pysed_hook() -> None:
    """Run a sed-like find and replace on files."""
    parser = argparse.ArgumentParser(
        description="Sed-like find and replace using Python.",
        prog="pysed",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        required=True,
        help="The pattern to search for",
    )
    parser.add_argument(
        "-r",
        "--replacement",
        required=True,
        help="The replacement string",
    )
    parser.add_argument(
        "-i",
        "--ignore-case",
        action="store_true",
        help="Make the search case insensitive",
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=file_existing,
        help="The files to operate on",
    )

    args = parser.parse_args()

    flags = 0
    if args.ignore_case:
        flags = re.IGNORECASE

    if _process_files(args.files, args.pattern, args.replacement, flags):
        sys.exit(1)


def _process_files(
    files: List[str],
    pattern: str,
    replacement: str,
    flags: int,
) -> bool:
    """Process the list of files and perform the replacement."""
    regex = re.compile(pattern, flags=flags)
    modified = False

    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        new_content = regex.sub(replacement, content)

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_content)
            modified = True

    return modified
