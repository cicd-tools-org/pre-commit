#!/bin/bash

# Commitizen 'pre_bump_hook' to make TOML quotes compatible with tomll.

# pre-commit script.

set -eo pipefail

# shellcheck source=./.cicd-tools/boxes/bootstrap/libraries/environment.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../../.cicd-tools/boxes/bootstrap/libraries/environment.sh"

# shellcheck source=./.cicd-tools/boxes/bootstrap/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../../.cicd-tools/boxes/bootstrap/libraries/logging.sh"

main() {
  environment -m "CZ_PRE_NEW_VERSION"
  log "INFO" "Standardizing versions in the pyproject.toml file ..."
  sed -i.bak "s,\"${CZ_PRE_NEW_VERSION}\",'${CZ_PRE_NEW_VERSION}',g" pyproject.toml
  rm pyproject.toml.bak
  log "INFO" "Ready to complete version bump!"
}

main "$@"
