"""Sphinx related pre-commit scripts."""

import argparse
import os
import sys

from .cli.types import dir_existing, dir_valid, language_code
from .system import call, git_ls_untracked, rmtree

SPHINX_DEFAULT_GETTEXT_FOLDER = "gettext"
SPHINX_DEFAULT_LOCALES_FOLDER = "locales"


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
        help="The build folder (can be inside or outside the source folder)",
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

    target_build_folder = os.path.join(args.build, args.language)
    rmtree(target_build_folder)

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


def sphinx_translate() -> None:
    """Extract translations for sphinx documentation."""
    parser = argparse.ArgumentParser(
        description="Extract translations for sphinx documentation.",
        prog="sphinx_translate",
    )
    parser.add_argument(
        "-b",
        "--build",
        required=True,
        type=dir_valid,
        help="The build folder (can be inside or outside the source folder)",
    )
    parser.add_argument(
        "-g",
        "--gettext",
        default=SPHINX_DEFAULT_GETTEXT_FOLDER,
        required=False,
        type=str,
        help="The build's gettext subfolder",
    )
    parser.add_argument(
        "-l",
        "--locales",
        default=SPHINX_DEFAULT_LOCALES_FOLDER,
        required=False,
        type=str,
        help="The sources's locales subfolder",
    )
    parser.add_argument(
        "-s",
        "--source",
        required=True,
        type=dir_existing,
        help="The documentation source folder",
    )

    args = parser.parse_args()

    gettext_folder = os.path.join(args.build, args.gettext)
    locales_folder = os.path.join(args.source, args.locales)
    rmtree(gettext_folder)

    os.environ.pop("VIRTUAL_ENV", None)

    call([
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "gettext",
        args.source,
        gettext_folder,
    ], )
    call([
        "poetry",
        "run",
        "sphinx-intl",
        "update",
        "-p",
        gettext_folder,
        "-d",
        locales_folder,
    ], )

    untracked_files = git_ls_untracked(locales_folder)
    if untracked_files:
        print("Untracked translation files detected:")
        for untracked_file in untracked_files:
            print(f"  {untracked_file}")
        sys.exit(1)
