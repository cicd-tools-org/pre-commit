"""Sphinx related pre-commit scripts."""

import argparse
import os

from .cli.types import existing_directory, language_code, valid_path
from .system import call


def sphinx_build_language() -> None:
    """Build sphinx documentation for a specific language."""
    parser = argparse.ArgumentParser(
        description="Build sphinx documentation for a specific language.",
    )
    parser.add_argument(
        "-l",
        "--language",
        required=True,
        type=language_code,
        help="The target language (e.g. en)",
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


def sphinx_translate() -> None:
    """Extract translations for sphinx documentation."""
    parser = argparse.ArgumentParser(
        description="Extract translations for sphinx documentation.",
    )
    parser.add_argument(
        "-d",
        "--documentation",
        required=True,
        type=existing_directory,
        help="The documentation folder",
    )

    args = parser.parse_args()

    call(["poetry", "run", "make", "gettext"], cwd=args.documentation)
    call(["poetry", "run", "sphinx-intl", "update"], cwd=args.documentation)
