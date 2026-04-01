"""Sphinx related pre-commit scripts."""

from __future__ import annotations

import argparse
import os

from .system import call


def sphinx_build_language() -> None:
    """Build sphinx documentation for a specific language."""
    parser = argparse.ArgumentParser(
        description="Build sphinx documentation for a specific language."
    )
    parser.add_argument(
        "-l", "--language", required=True, help="The target language (e.g. EN)"
    )
    parser.add_argument(
        "-t", "--source", required=True, help="The source folder"
    )
    parser.add_argument(
        "-b", "--build", required=True, help="The build folder"
    )

    args = parser.parse_args()

    if len(args.language) != 2:
        parser.error(
            f"Language '{args.language}' must be a 2 character string."
        )

    if not os.path.isdir(args.source):
        parser.error(f"Source folder '{args.source}' does not exist.")

    if not os.path.exists(os.path.dirname(os.path.abspath(args.build))):
        parser.error(f"Build folder path '{args.build}' is not valid.")

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
