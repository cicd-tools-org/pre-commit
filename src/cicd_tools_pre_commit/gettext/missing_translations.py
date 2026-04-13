"""Identify missing translations in PO files."""

from __future__ import annotations

import argparse
import sys

from cicd_tools_pre_commit.cli.types import file_existing

PO_COMMENT_IDENTIFIER = "#"
PO_MSGID_HEADER_IDENTIFIER = 'msgid ""'
PO_MSGID_IDENTIFIER = "msgid "
PO_MSGSTR_EMPTY_IDENTIFIER = 'msgstr ""'
PO_STRING_IDENTIFIER = '"'


def gettext_translations_missing_hook() -> None:
    """Check for missing translations in PO files."""
    parser = argparse.ArgumentParser(
        description="Check for missing translations in PO files.",
        prog="gettext_translations_missing",
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
        missing_msgids = missing_translations(filepath)
        if missing_msgids:
            error_found = True
            print(f"Missing translations in '{filepath}':")
            for msgid in missing_msgids:
                print(f"  {msgid}")

    if error_found:
        sys.exit(1)


def missing_translations(filepath: str) -> list[str]:
    """Identify missing translations in a PO file."""
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    missing_msgids = []
    for i, line in enumerate(lines):
        if line.strip() == PO_MSGSTR_EMPTY_IDENTIFIER:
            if _is_multi_line_msgstr(lines, i):
                continue

            msgid = _find_msgid_for_line(lines, i)

            if msgid == PO_MSGID_HEADER_IDENTIFIER:
                continue

            if msgid:
                missing_msgids.append(msgid)
            else:
                missing_msgids.append(f"Unknown msgid near line {i + 1}")

    return missing_msgids


def _is_multi_line_msgstr(lines: list[str], index: int) -> bool:
    """Check if the msgstr at the given index is multi-line."""
    return (index + 1 < len(lines)
            and lines[index + 1].strip().startswith(PO_STRING_IDENTIFIER))


def _find_msgid_for_line(lines: list[str], index: int) -> str:
    """Find the full msgid preceding the given line index."""
    msgid_lines = []
    for j in range(index - 1, -1, -1):
        line = lines[j].strip()
        if not line or line.startswith(PO_COMMENT_IDENTIFIER):
            if msgid_lines:
                break
            continue

        if line.startswith(PO_MSGID_IDENTIFIER):
            msgid_lines.insert(0, line)
            break

        if line.startswith(PO_STRING_IDENTIFIER):
            msgid_lines.insert(0, line)

    return " ".join(msgid_lines)
