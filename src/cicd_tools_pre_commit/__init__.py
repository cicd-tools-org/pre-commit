"""Expose the CICD-Tools pre-commit resources."""

import os
import shlex
import sys

RESOURCES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "cicd-tools",
)
RESOURCES_PATH_ENV_VAR = "CICD_RESOURCES"


def main() -> None:
    variable_definition = "{%s}" % RESOURCES_PATH_ENV_VAR
    for index, arg in enumerate(sys.argv):
        if variable_definition in arg:
            sys.argv[index] = sys.argv[index].format(
                **{RESOURCES_PATH_ENV_VAR: RESOURCES_PATH}
            )
    os.system(shlex.join(sys.argv[1:]))
