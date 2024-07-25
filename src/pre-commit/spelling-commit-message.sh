#!/bin/bash

# Runs vale on the specified commit message file, with the Git content filtered out.

# 1:  The Docker image and tag to use.
# 2:  The commit message file to lint.

# pre-commit script.

set -eo pipefail

# shellcheck source=./../cicd-tools/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/logging.sh"

# shellcheck source=./../cicd-tools/libraries/container.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/container.sh"

main() {
  local PRECOMMIT_GIT_COMMIT_MESSAGE_FILE
  local PRECOMMIT_GIT_CONTENT_REGEX
  local PRECOMMIT_VALE_DOCKER_IMAGE

  PRECOMMIT_GIT_COMMIT_MESSAGE_FILE="${2}"
  PRECOMMIT_GIT_CONTENT_REGEX='/^#[[:blank:]]*.*$/d'
  PRECOMMIT_VALE_DOCKER_IMAGE="${1}"

  log "INFO" "Checking commit message spelling..."

  log "DEBUG" "Docker Image: '${PRECOMMIT_VALE_DOCKER_IMAGE}'"
  log "DEBUG" "Commit Message: '${PRECOMMIT_GIT_COMMIT_MESSAGE_FILE}'"
  sed "${PRECOMMIT_GIT_CONTENT_REGEX}" "${PRECOMMIT_GIT_COMMIT_MESSAGE_FILE}"
  log "DEBUG" "Running vale ..."
  container_cache_image "${PRECOMMIT_VALE_DOCKER_IMAGE}"
  sed "${PRECOMMIT_GIT_CONTENT_REGEX}" "${PRECOMMIT_GIT_COMMIT_MESSAGE_FILE}" |
    container "${PRECOMMIT_VALE_DOCKER_IMAGE}" vale

  log "INFO" "Commit message spelling has passed!"
}

main "$@"
