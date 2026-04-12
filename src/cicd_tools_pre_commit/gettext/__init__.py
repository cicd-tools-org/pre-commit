"""Gettext related pre-commit scripts."""

from .missing_translations import gettext_translations_missing_hook

__all__ = ("gettext_translations_missing_hook",)
