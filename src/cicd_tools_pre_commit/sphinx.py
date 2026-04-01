"""Sphinx related pre-commit scripts."""

import argparse
import os

from .cli.types import dir_existing, dir_valid, language_code
from .system import call


def sphinx_build_language() -> None:
    """Build sphinx documentation for a specific language."""
    parser = argparse.ArgumentParser(
        description="Build sphinx documentation for a specific language.",
        prog="sphinx_build_language",
    )
    parser.add_argument(
        "-b",
        "--build",
        required=True,
        type=dir_valid,
        help="The build folder (relative to the source folder)",
    )
    parser.add_argument(
        "-l",
        "--language",
        required=True,
        type=language_code,
        help="The target language (e.g. en)",
    )
    parser.add_argument(
        "-s",
        "--source",
        required=True,
        type=dir_existing,
        help="The documentation source folder",
    )

    args = parser.parse_args()

    target_build_folder = os.path.join(args.source, args.build, args.language)

    os.environ.pop("VIRTUAL_ENV", None)

    call([
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
    ])
