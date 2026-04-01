"""Sphinx related pre-commit scripts."""

from __future__ import annotations

import argparse
import os

from .system import call
from .system.argparse_types import existing_directory, valid_path


def sphinx_build_language() -> None:
    """Build sphinx documentation for a specific language."""
    parser = argparse.ArgumentParser(
        description="Build sphinx documentation for a specific language."
    )
    parser.add_argument(
        "-l", "--language", required=True, help="The target language (e.g. EN)"
    )
    parser.add_argument(
        "-t",
        "--source",
        required=True,
        type=existing_directory,
        help="The source folder",
    )
    parser.add_argument(
        "-b",
        "--build",
        required=True,
        type=valid_path,
        help="The build folder",
    )

    args = parser.parse_args()

    if len(args.language) != 2:
        parser.error(
            f"Language '{args.language}' must be a 2 character string."
        )

    target_build_folder = os.path.join(args.build, args.language)
    command = [
        "poetry",
        "run",
        "sphinx-build",
        "-Ea",
        "-b",
        "html",
        "-D",
        f"language={args.language}",
        args.source,
        target_build_folder,
    ]

    call(command)


if __name__ == "__main__":
    sphinx_build_language()
