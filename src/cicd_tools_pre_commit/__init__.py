"""CICD-Tools pre-commit scripts."""

from .resources import with_cicd_resources
from .sphinx import sphinx_build_language

__all__ = (
    "sphinx_build_language",
    "with_cicd_resources",
)
