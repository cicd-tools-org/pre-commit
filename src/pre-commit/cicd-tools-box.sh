#!/bin/bash

# Remote toolbox downloader.
# Requires gpg binary: https://gnupg.org/

# pre-commit script.

set -eo pipefail

TOOLBOX_PATH=".cicd-tools"
TOOLBOX_ABSOLUTE_PATH="${PWD}/${TOOLBOX_PATH}"
TOOLBOX_REMOTES_FOLDER="boxes"
TOOLBOX_MANIFEST_FILE="${TOOLBOX_PATH}/manifest.json"

# shellcheck source=./../cicd-tools/libraries/container.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/container.sh"

# shellcheck source=./../cicd-tools/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/logging.sh"

main() {
  local TOOLBOX_DOCKER_IMAGE_CURL="system"
  local TOOLBOX_DOCKER_IMAGE_GPG="system"
  local TOOLBOX_DOCKER_IMAGE_JQ="system"
  local TOOLBOX_DOWNLOAD_MAX_TIME="30"
  local TOOLBOX_DOWNLOAD_RETRIES="3"
  local TOOLBOX_GPG_SESSION_ID="cicd-tools-gpg1"
  local TOOLBOX_MANIFEST_ASC
  local TOOLBOX_MANIFEST_DISABLE_SECURITY="false"
  local TOOLBOX_TARGET_URL
  local TOOLBOX_TARGET_VERSION
  local TOOLBOX_TEMP_DIRECTORY

  _toolbox_args "$@"

  TOOLBOX_TEMP_DIRECTORY="$(mktemp -d "./tmp.XXXXXXXXX")"

  # shellcheck disable=SC2064
  trap "rm -rf \"${TOOLBOX_TEMP_DIRECTORY}\"" EXIT

  container_cache_image "${TOOLBOX_DOCKER_IMAGE_CURL}"
  container_cache_image "${TOOLBOX_DOCKER_IMAGE_GPG}"
  container_cache_image "${TOOLBOX_DOCKER_IMAGE_JQ}"

  _toolbox_manifest_download
  _toolbox_manifest_load
  _toolbox_box_download
  _toolbox_box_checksum
  _toolbox_box_install
}

_toolbox_args() {
  local OPTARG
  local OPTIND
  local OPTION

  while getopts "b:c:g:j:m:r:t:" OPTION; do
    case "$OPTION" in
      b)
        TOOLBOX_TARGET_VERSION="${OPTARG}"
        TARGET_TOOLBOX_FILENAME="${TOOLBOX_TARGET_VERSION}.tar.gz"
        ;;
      c)
        TOOLBOX_DOCKER_IMAGE_CURL="${OPTARG}"
        ;;
      g)
        TOOLBOX_DOCKER_IMAGE_GPG="${OPTARG}"
        ;;
      j)
        TOOLBOX_DOCKER_IMAGE_JQ="${OPTARG}"
        ;;
      m)
        TOOLBOX_MANIFEST_ASC="${OPTARG}"
        ;;
      r)
        TOOLBOX_DOWNLOAD_MAX_TIME="${OPTARG}"
        ;;
      t)
        TOOLBOX_DOWNLOAD_MAX_TIME="${OPTARG}"
        ;;
      \?)
        _toolbox_usage
        ;;
      :)
        _toolbox_usage
        ;;
      *)
        _toolbox_usage
        ;;
    esac
  done
  shift $((OPTIND - 1))

  if [[ -z "${TOOLBOX_TARGET_VERSION}" ]] ||
    [[ -z "${TOOLBOX_MANIFEST_ASC}" ]]; then
    _toolbox_usage
  fi
}

_toolbox_box_checksum() {
  pushd "${TOOLBOX_TEMP_DIRECTORY}" >> /dev/null
  if [[ "${TOOLBOX_MANIFEST_DISABLE_SECURITY}" == "false" ]]; then
    if ! echo "${TARGET_TOOLBOX_SHA}  ${TARGET_TOOLBOX_FILENAME}" | sha256sum -c; then
      log "ERROR" "CHECKSUM > Hash of remote file does not match!"
      log "ERROR" "CHECKSUM > Cannot proceed."
      exit 127
    else
      log "INFO" "CHECKSUM > Hash verification has passed."
    fi
  else
    log "WARNING" "CHECKSUM > The manifest has DISABLED all checksum validation."
  fi
  cp "${TARGET_TOOLBOX_FILENAME}" "${TOOLBOX_ABSOLUTE_PATH}/${TOOLBOX_REMOTES_FOLDER}"
  popd >> /dev/null
}

_toolbox_box_download() {
  if [[ -f "${TOOLBOX_PATH}/${TOOLBOX_REMOTES_FOLDER}/${TARGET_TOOLBOX_FILENAME}" ]]; then
    mv "${TOOLBOX_PATH}/${TOOLBOX_REMOTES_FOLDER}/${TARGET_TOOLBOX_FILENAME}" "${TOOLBOX_TEMP_DIRECTORY}"
    log "WARNING" "BOX > Toolbox Version ${TOOLBOX_TARGET_VERSION} has already been downloaded."
  else
    _toolbox_box_fetch
  fi
}

_toolbox_box_fetch() {
  log "DEBUG" "BOX > Target Toolbox Version: ${TOOLBOX_TARGET_VERSION}"
  log "DEBUG" "BOX > Target Toolbox SHA: ${TARGET_TOOLBOX_SHA}"
  log "DEBUG" "BOX > Target Toolbox URL: ${TOOLBOX_TARGET_URL}"

  mkdir -p "${TOOLBOX_PATH}/${TOOLBOX_REMOTES_FOLDER}"

  pushd "${TOOLBOX_TEMP_DIRECTORY}" >> /dev/null
  _toolbox_fetch "${TOOLBOX_TARGET_URL}" > "${TARGET_TOOLBOX_FILENAME}"
  popd >> /dev/null

  log "INFO" "BOX > Remote toolbox retrieved."
}

_toolbox_box_install() {
  pushd "${TOOLBOX_PATH}/${TOOLBOX_REMOTES_FOLDER}" >> /dev/null
  tar xvzf "${TARGET_TOOLBOX_FILENAME}"
  log "DEBUG" "BOX > Toolbox Version ${TOOLBOX_TARGET_VERSION} has been installed to ${TOOLBOX_PATH}/${TOOLBOX_REMOTES_FOLDER}."
  if [[ -e active ]]; then
    rm active
  fi
  ln -sf "${TOOLBOX_TARGET_VERSION}" active
  log "INFO" "BOX > Toolbox Version ${TOOLBOX_TARGET_VERSION} has been activated."
  popd >> /dev/null
}

_toolbox_fetch() {
  # 1: url
  log "DEBUG" "FETCH > URL: ${1}"
  log "DEBUG" "FETCH > Retries: ${TOOLBOX_DOWNLOAD_RETRIES}"
  log "DEBUG" "FETCH > Max Time: ${TOOLBOX_DOWNLOAD_MAX_TIME}"

  container \
    "${TOOLBOX_DOCKER_IMAGE_CURL}" \
    curl \
    --fail \
    --location \
    --silent \
    --show-error \
    --retry "${TOOLBOX_DOWNLOAD_RETRIES}" \
    --retry-max-time "${TOOLBOX_DOWNLOAD_MAX_TIME}" \
    "${1}"

  log "DEBUG" "FETCH > Fetch complete."
}

_toolbox_manifest_download() {
  _toolbox_fetch \
    "${TOOLBOX_MANIFEST_ASC}" \
    > "${TOOLBOX_TEMP_DIRECTORY}/manifest.asc"

  container_session_run \
    "${TOOLBOX_GPG_SESSION_ID}" \
    "${TOOLBOX_DOCKER_IMAGE_GPG}" \
    gpg \
    --yes \
    --output \
    "${TOOLBOX_MANIFEST_FILE}" \
    --verify "${TOOLBOX_TEMP_DIRECTORY}/manifest.asc"

  container_session_destroy \
    "${TOOLBOX_GPG_SESSION_ID}" \
    "${TOOLBOX_DOCKER_IMAGE_GPG}"

  log "INFO" "MANIFEST > Remote manifest retrieved."
}

_toolbox_manifest_load() {
  _toolbox_manifest_read_is_version_present
  TARGET_TOOLBOX_SHA="$(_toolbox_manifest_read_toolbox_sha)"
  TOOLBOX_MANIFEST_DISABLE_SECURITY="$(_toolbox_manifest_read_is_security_disabled)"
  TOOLBOX_TARGET_URL="$(_toolbox_manifest_read_toolbox_url)"

  log "INFO" "MANIFEST > Remote manifest loaded."
}

_toolbox_manifest_read_is_version_present() {
  # shellcheck disable=SC2016
  if ! container \
    "${TOOLBOX_DOCKER_IMAGE_JQ}" \
    jq \
    --arg \
    version \
    "${TOOLBOX_TARGET_VERSION}.tar.gz" \
    -erM '.manifest[$version]' \
    "${TOOLBOX_MANIFEST_FILE}" \
    > /dev/null; then
    log "ERROR" "MANIFEST > Toolbox version '${TOOLBOX_TARGET_VERSION}' is not in the manifest."
    exit 127
  fi
}

_toolbox_manifest_read_is_security_disabled() {
  container \
    "${TOOLBOX_DOCKER_IMAGE_JQ}" \
    jq \
    -rM \
    ".disable_security" \
    "${TOOLBOX_MANIFEST_FILE}"
}

_toolbox_manifest_read_toolbox_sha() {
  # shellcheck disable=SC2016
  container \
    "${TOOLBOX_DOCKER_IMAGE_JQ}" \
    jq \
    --arg \
    version \
    "${TOOLBOX_TARGET_VERSION}.tar.gz" \
    -erM '.manifest[$version]' \
    "${TOOLBOX_MANIFEST_FILE}"
}

_toolbox_manifest_read_toolbox_url() {
  echo "$(_toolbox_manifest_read_toolbox_url_prefix)/${TOOLBOX_TARGET_VERSION}.tar.gz"
}

_toolbox_manifest_read_toolbox_url_prefix() {
  local TOOLBOX_MANIFEST_REMOTE_SHA
  local TOOLBOX_MANIFEST_REMOTE_SOURCE
  local TOOLBOX_MANIFEST_REMOTE_PATH

  TOOLBOX_MANIFEST_REMOTE_SHA="$(container "${TOOLBOX_DOCKER_IMAGE_JQ}" jq -erM '.version' "${TOOLBOX_MANIFEST_FILE}")"
  TOOLBOX_MANIFEST_REMOTE_SOURCE="$(container "${TOOLBOX_DOCKER_IMAGE_JQ}" jq -erM '.source' "${TOOLBOX_MANIFEST_FILE}")"
  TOOLBOX_MANIFEST_REMOTE_PATH="$(container "${TOOLBOX_DOCKER_IMAGE_JQ}" jq -erM '.toolbox_path' "${TOOLBOX_MANIFEST_FILE}")"
  echo "${TOOLBOX_MANIFEST_REMOTE_SOURCE}/${TOOLBOX_MANIFEST_REMOTE_SHA}/${TOOLBOX_MANIFEST_REMOTE_PATH}"
}

_toolbox_usage() {
  log "ERROR" "cicd-tools-box.sh -- download a remote toolbox from the CICD-Tools manifest."
  log "ERROR" "----------------------------------------------------------------------------"
  log "ERROR" "cicd-tools-box.sh"
  log "ERROR" "           -b [TOOLBOX VERSION]"
  log "ERROR" "           -c (OPTIONAL CURL DOCKER IMAGE)"
  log "ERROR" "           -g (OPTIONAL GPG DOCKER IMAGE)"
  log "ERROR" "           -j (OPTIONAL JQ DOCKER IMAGE)"
  log "ERROR" "           -m [REMOTE MANIFEST URL]"
  log "ERROR" "           -r (OPTIONAL RETRY COUNT)"
  log "ERROR" "           -t (OPTIONAL MAX RETRY TIME)"
  exit 127
}

main "$@"
