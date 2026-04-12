"""Identify missing translations in PO files."""

from __future__ import annotations

import argparse
import sys

from ..cli.types import file_existing

_COMMENT_ID = "#"
_MSGID_ID = "msgid "
_MSGSTR_ID = 'msgstr ""'
_STRING_ID = '"'


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
        missing_msgids = _process_file(filepath)
        if missing_msgids:
            error_found = True
            print(f"Missing translations in '{filepath}':")
            for msgid in missing_msgids:
                print(f"  {msgid}")

    if error_found:
        sys.exit(1)


def _process_file(filepath: str) -> list[str]:
    """Identify missing translations in a PO file."""
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    missing_msgids = []
    for i, line in enumerate(lines):
        if line.strip() == _MSGSTR_ID:
            if _is_multi_line_msgstr(lines, i):
                continue

            msgid = _find_msgid_for_line(lines, i)

            # Skip header entry (empty msgid)
            if msgid == f'{_MSGID_ID.strip()} ""':
                continue

            if msgid:
                missing_msgids.append(msgid)
            else:
                missing_msgids.append(f"Unknown msgid near line {i + 1}")

    return missing_msgids


def _is_multi_line_msgstr(lines: list[str], index: int) -> bool:
    """Check if the msgstr at the given index is multi-line."""
    return (index + 1 < len(lines)
            and lines[index + 1].strip().startswith(_STRING_ID))


def _find_msgid_for_line(lines: list[str], index: int) -> str:
    """Find the full msgid preceding the given line index."""
    msgid_parts = []
    for j in range(index - 1, -1, -1):
        line = lines[j].strip()
        if not line or line.startswith(_COMMENT_ID):
            if msgid_parts:
                break
            continue

        if line.startswith(_MSGID_ID):
            msgid_parts.insert(0, line)
            break

        if line.startswith(_STRING_ID):
            msgid_parts.insert(0, line)

    return " ".join(msgid_parts)
