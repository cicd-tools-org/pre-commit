"""CICD-Tools pre-commit scripts."""

from .gettext import gettext_translations_missing_hook
from .pysed import pysed_hook
from .resources import with_cicd_resources
from .sphinx import sphinx_build_language, sphinx_translate

__all__ = (
    "gettext_translations_missing_hook",
    "pysed_hook",
    "sphinx_build_language",
    "sphinx_translate",
    "with_cicd_resources",
)
