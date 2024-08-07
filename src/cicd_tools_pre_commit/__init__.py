"""Expose the CICD-Tools pre-commit resources."""

import os
import shlex
import sys

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


def main() -> None:
    if len(sys.argv) < 2:
        raise Exception(INSUFFICIENT_ARGUMENTS_ERROR)

    variable_definition = "{%s}" % RESOURCES_VARIABLE_NAME
    for index, arg in enumerate(sys.argv):
        if variable_definition in arg:
            sys.argv[index] = sys.argv[index].format(
                **{RESOURCES_VARIABLE_NAME: RESOURCES_PATH}
            )
    os.system(shlex.join(sys.argv[1:]))
