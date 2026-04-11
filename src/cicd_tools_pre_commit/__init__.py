"""CICD-Tools pre-commit scripts."""

from .pysed import main as pysed
from .resources import with_cicd_resources
from .sphinx import sphinx_build_language, sphinx_translate

__all__ = (
    "pysed",
    "sphinx_build_language",
    "sphinx_translate",
    "with_cicd_resources",
)
