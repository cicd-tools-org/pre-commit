#!/bin/bash

# Runs yq on the specified pre-commit configuration file to sort the order of the hooks by id.

# 1:  The Docker image and tag to use.
# @:  An array of pre-commit configuration files to sort.

# pre-commit script.

set -eo pipefail

# shellcheck source=./../cicd-tools/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/logging.sh"

# shellcheck source=./../cicd-tools/libraries/container.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/container.sh"

main() {
  local PRECOMMIT_INPUT_FILE
  local PRECOMMIT_YQ_DOCKER_IMAGE

  PRECOMMIT_YQ_DOCKER_IMAGE="${1}"
  shift

  log "INFO" "Sorting pre-commit hook definition files ..."
  log "DEBUG" "Docker Image: '${PRECOMMIT_YQ_DOCKER_IMAGE}'"

  container_cache_image "${PRECOMMIT_YQ_DOCKER_IMAGE}"

  for PRECOMMIT_INPUT_FILE in "${@}"; do
    container "${PRECOMMIT_YQ_DOCKER_IMAGE}" \
      yq \
      --inplace \
      '. |= sort_by(.id)' \
      "${PRECOMMIT_INPUT_FILE}"
  done

  log "INFO" "Sorting has completed successfully!"
}

main "$@"
