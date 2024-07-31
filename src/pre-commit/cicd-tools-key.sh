#!/bin/bash

# Remote gpg key verification.
# Requires gpg binary: https://gnupg.org/

# CICD-Tools script.

set -eo pipefail

# shellcheck source=./../cicd-tools/libraries/container.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/container.sh"

# shellcheck source=./../cicd-tools/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/logging.sh"

# shellcheck source=./../cicd-tools/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/override.sh"

main() {
  local TOOLBOX_GPG_DECRYPTED_FILE
  local TOOLBOX_GPG_DOCKER_IMAGE="system"
  local TOOLBOX_GPG_ENCRYPTED_FILE
  local TOOLBOX_GPG_KEYSERVER_PRIMARY
  local TOOLBOX_GPG_KEYSERVER_SECONDARY
  local TOOLBOX_GPG_KEY_NAME
  local TOOLBOX_GPG_SESSION_ID="cicd-tools-gpg1"
  local TOOLBOX_GPG_TEMP_DIRECTORY

  TOOLBOX_GPG_DECRYPTED_FILE="$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/pgp/verification.txt"
  TOOLBOX_GPG_ENCRYPTED_FILE="$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/pgp/verification.sign"

  _toolbox_gpg_args "$@"

  override \
    -o "TOOLBOX_OVERRIDE_DOCKER_IMAGE_GPG TOOLBOX_OVERRIDE_GPG_KEY_SERVER_PRIMARY TOOLBOX_OVERRIDE_GPG_KEY_SERVER_SECONDARY TOOLBOX_OVERRIDE_GPG_KEY_NAME" \
    -t "TOOLBOX_GPG_DOCKER_IMAGE TOOLBOX_GPG_KEYSERVER_PRIMARY TOOLBOX_GPG_KEYSERVER_SECONDARY TOOLBOX_GPG_KEY_NAME"

  if [[ -z "${TOOLBOX_GPG_DECRYPTED_FILE}" ]] ||
    [[ -z "${TOOLBOX_GPG_DOCKER_IMAGE}" ]] ||
    [[ -z "${TOOLBOX_GPG_ENCRYPTED_FILE}" ]] ||
    [[ -z "${TOOLBOX_GPG_KEY_NAME}" ]] ||
    [[ -z "${TOOLBOX_GPG_KEYSERVER_PRIMARY}" ]]; then
    _toolbox_gpg_usage
  fi

  TOOLBOX_GPG_TEMP_DIRECTORY="$(mktemp -d "./tmp.XXXXXXXXX")"

  # shellcheck disable=SC2064
  trap "rm -rf \"${TOOLBOX_GPG_TEMP_DIRECTORY}\"" EXIT

  container_cache_image "${TOOLBOX_GPG_DOCKER_IMAGE}"

  _toolbox_gpg_verify_signature_files

  _toolbox_gpg_import_key
  log "INFO" "Key '${TOOLBOX_GPG_KEY_NAME}' has been imported!"

  _toolbox_gpg_verify_key
  log "INFO" "Key '${TOOLBOX_GPG_KEY_NAME}' has passed verification!"

  _toolbox_gpg_trust_key
  log "INFO" "Key '${TOOLBOX_GPG_KEY_NAME}' is now trusted."
}

_toolbox_gpg_args() {
  local OPTARG
  local OPTIND
  local OPTION

  while getopts "d:e:g:n:p:s:" OPTION; do
    case "$OPTION" in
      d)
        TOOLBOX_GPG_DECRYPTED_FILE="${OPTARG}"
        ;;
      e)
        TOOLBOX_GPG_ENCRYPTED_FILE="${OPTARG}"
        ;;
      g)
        TOOLBOX_GPG_DOCKER_IMAGE="${OPTARG}"
        ;;
      n)
        TOOLBOX_GPG_KEY_NAME="${OPTARG}"
        ;;
      p)
        TOOLBOX_GPG_KEYSERVER_PRIMARY="${OPTARG}"
        ;;
      s)
        TOOLBOX_GPG_KEYSERVER_SECONDARY="${OPTARG}"
        ;;
      \?)
        _toolbox_gpg_usage
        ;;
      :)
        _toolbox_gpg_usage
        ;;
      *)
        _toolbox_gpg_usage
        ;;
    esac
  done
  shift $((OPTIND - 1))
}

_toolbox_gpg_import_key() {
  container_session_create \
    "${TOOLBOX_GPG_SESSION_ID}" \
    "${TOOLBOX_GPG_DOCKER_IMAGE}"

  container_session_run \
    "${TOOLBOX_GPG_SESSION_ID}" \
    "${TOOLBOX_GPG_DOCKER_IMAGE}" \
    gpg \
    --keyserver "${TOOLBOX_GPG_KEYSERVER_PRIMARY}" \
    --recv-key "${TOOLBOX_GPG_KEY_NAME}" && return 0

  if [[ -z "${TOOLBOX_GPG_KEYSERVER_SECONDARY}" ]]; then
    log "ERROR" "Failed to import from the primary key server and no secondary was specified."
    return 127
  fi

  container_session_run \
    "${TOOLBOX_GPG_SESSION_ID}" \
    "${TOOLBOX_GPG_DOCKER_IMAGE}" \
    gpg \
    --keyserver "${TOOLBOX_GPG_KEYSERVER_SECONDARY}" \
    --recv-key "${TOOLBOX_GPG_KEY_NAME}"
}

_toolbox_gpg_verify_signature_files() {
  if [[ ! -f "${TOOLBOX_GPG_DECRYPTED_FILE}" ]]; then
    log "ERROR" "The decrypted signature verification file '${TOOLBOX_GPG_DECRYPTED_FILE}' was not found!"
    exit 127
  fi
  if [[ ! -f "${TOOLBOX_GPG_ENCRYPTED_FILE}" ]]; then
    log "ERROR" "The encrypted signature verification file '${TOOLBOX_GPG_ENCRYPTED_FILE}' was not found!"
    exit 127
  fi
  cp "${TOOLBOX_GPG_DECRYPTED_FILE}" "${TOOLBOX_GPG_TEMP_DIRECTORY}/verification.txt"
  cp "${TOOLBOX_GPG_ENCRYPTED_FILE}" "${TOOLBOX_GPG_TEMP_DIRECTORY}/verification.sign"
}

_toolbox_gpg_verify_key() {
  if ! container_session_run \
    "${TOOLBOX_GPG_SESSION_ID}" \
    "${TOOLBOX_GPG_DOCKER_IMAGE}" \
    gpg \
    --verify "${TOOLBOX_GPG_TEMP_DIRECTORY}/verification.sign" \
    "${TOOLBOX_GPG_TEMP_DIRECTORY}/verification.txt"; then
    log "ERROR" "Key '${TOOLBOX_GPG_KEY_NAME}' has failed verification!"
    exit 127
  fi
}

_toolbox_gpg_trust_key() {
  container_session_run \
    "${TOOLBOX_GPG_SESSION_ID}" \
    "${TOOLBOX_GPG_DOCKER_IMAGE}" \
    bash -c "echo \"${TOOLBOX_GPG_KEY_NAME}:6:\" | gpg --import-ownertrust"
}

_toolbox_gpg_usage() {
  log "ERROR" "cicd-tools-key.sh -- download a remote toolbox from the CICD-Tools manifest."
  log "ERROR" "----------------------------------------------------------------------------"
  log "ERROR" "cicd-tools-key.sh"
  log "ERROR" "           -d (OPTIONAL USER SUPPLIED DECRYPTED SIGNATURE VERIFICATION FILE)"
  log "ERROR" "           -e (OPTIONAL USER SUPPLIED ENCRYPTED SIGNATURE VERIFICATION FILE)"
  log "ERROR" "           -g (OPTIONAL GPG DOCKER IMAGE)"
  log "ERROR" "           -n [KEY NAME]"
  log "ERROR" "           -p [PRIMARY KEY SERVER]"
  log "ERROR" "           -s (OPTIONAL SECONDARY KEY SERVER)"
  exit 127
}

main "$@"
