"""Gettext related pre-commit scripts."""

from __future__ import annotations

import argparse
import sys

from .cli.types import file_existing


def missing_translations(filepath: str) -> list[str]:
    """Identify missing translations in a PO file."""
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    missing = []
    for i, line in enumerate(lines):
        if line.strip() == 'msgstr ""':
            # Check if it's the start of a multi-line translation
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('"'):
                continue

            # Identify the msgid for the missing translation
            msgid_lines = []
            for j in range(i - 1, -1, -1):
                prev_line = lines[j].strip()
                if not prev_line:
                    if msgid_lines:
                        break
                    continue

                if prev_line.startswith("#"):
                    continue

                if prev_line.startswith("msgid "):
                    msgid_lines.insert(0, prev_line)
                    break

                if prev_line.startswith('"'):
                    msgid_lines.insert(0, prev_line)

            full_msgid = " ".join(msgid_lines)

            # The header entry has an empty msgid ("")
            if full_msgid == 'msgid ""':
                continue

            if full_msgid:
                missing.append(full_msgid)
            else:
                missing.append(f"Unknown msgid near line {i + 1}")

    return missing


def missing_translations_hook() -> None:
    """Check for missing translations in PO files."""
    parser = argparse.ArgumentParser(
        description="Check for missing translations in PO files.",
        prog="missing_translations",
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=file_existing,
        help="The PO files to check",
    )

    args = parser.parse_args()

    error_found = False
    for filepath in args.files:
        missing = missing_translations(filepath)
        if missing:
            error_found = True
            print(f"Missing translations in '{filepath}':")
            for msgid in missing:
                print(f"  {msgid}")

    if error_found:
        sys.exit(1)
