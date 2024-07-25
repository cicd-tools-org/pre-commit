#!/bin/bash

# Runs ansible-galaxy to install/update the dependencies if needed, and then runs ansible-lint on each active target folder's changes.

# @:  An array of folders to run ansible-lint on.

# pre-commit script.

set -eo pipefail

# shellcheck source=./../cicd-tools/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/logging.sh"

# shellcheck source=./../cicd-tools/libraries/tools.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/tools.sh"

main() {
  local TARGET_FOLDERS=${*-"."}
  for TARGET in ${TARGET_FOLDERS}; do
    log "INFO" "Moving to target folder: '${TARGET}' ..."
    pushd "${TARGET}" >> /dev/null
    log "DEBUG" "  Executing 'ansible-lint' ..."
    cicd_tools "poetry" ansible-lint
    popd >> /dev/null
  done
}

main "$@"
