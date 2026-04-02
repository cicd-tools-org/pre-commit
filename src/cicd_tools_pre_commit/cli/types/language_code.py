"""language_code argparse type."""

import argparse
import re

LANGUAGE_CODE_REGEX = re.compile(r"^[a-z]{2}(_[A-Z]{2})?$")


def language_code(code: str) -> str:
    """Check if the language code matches the allowed pattern."""
    if not LANGUAGE_CODE_REGEX.match(code):
        raise argparse.ArgumentTypeError(
            f"Language code '{code}' is invalid. "
            "Expected format like 'en' or 'zh_CN'.",
        )
    return code
