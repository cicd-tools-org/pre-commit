"""Expose the CICD-Tools pre-commit resources."""

from __future__ import annotations

import os
import sys

from .system import call

RESOURCES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "cicd-tools",
)
RESOURCES_VARIABLE_NAME = "CICD_RESOURCES"
INSUFFICIENT_ARGUMENTS_ERROR = (
    "INSUFFICIENT ARGUMENTS:\n"
    "Please specify a program to execute, and additional arguments for that "
    "program.\n"
    "These arguments may reference paths starting with '{%s}/...' to access "
    "resources found in the CICD-Tools pre-commit repository's 'src' folder."
) % RESOURCES_VARIABLE_NAME


def with_cicd_resources() -> None:
    """Interpolate the CICD-Tools resource folder prior to execution."""
    if len(sys.argv) < 2:
        raise Exception(INSUFFICIENT_ARGUMENTS_ERROR)

    variable_definition = "{%s}" % RESOURCES_VARIABLE_NAME
    for index, arg in enumerate(sys.argv):
        if variable_definition in arg:
            sys.argv[index] = sys.argv[index].format(
                **{RESOURCES_VARIABLE_NAME: RESOURCES_PATH})

    call(sys.argv[1:])
