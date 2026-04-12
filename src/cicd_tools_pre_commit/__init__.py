"""CICD-Tools pre-commit scripts."""

from .gettext import missing_translations_hook
from .pysed import pysed_hook
from .resources import with_cicd_resources
from .sphinx import sphinx_build_language, sphinx_translate

__all__ = (
    "missing_translations_hook",
    "pysed_hook",
    "sphinx_build_language",
    "sphinx_translate",
    "with_cicd_resources",
)
