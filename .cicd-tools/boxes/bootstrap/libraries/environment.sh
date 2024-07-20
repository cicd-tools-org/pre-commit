#!/bin/bash

# Library for enforcing optional and mandatory environment variables.

set -eo pipefail

# shellcheck source=/dev/null
source "$(dirname -- "${BASH_SOURCE[0]}")/logging.sh"

environment() {
  local MANDATORY=()
  local OPTIONAL=()
  local DEFAULTS=()

  log "DEBUG" "${BASH_SOURCE[0]} '$*'"

  _environment_args "$@"
  _environment_set_defaults
}

_environment_args() {
  local OPTARG
  local OPTIND
  local OPTION

  while getopts "d:o:m:" OPTION; do
    case "$OPTION" in
      d)
        _environment_parse_defaults "${OPTARG}"
        ;;
      o)
        _environment_parse_optional "${OPTARG}"
        ;;
      m)
        _environment_parse_mandatory "${OPTARG}"
        ;;
      \?)
        _environment_usage
        ;;
      :)
        _environment_usage
        ;;
    esac
  done

  if [[ "${#OPTIONAL[@]}" -ne "${#DEFAULTS[@]}" ]]; then
    log "ERROR" "ENVIRONMENT > You must specify the same number of DEFAULT values and OPTIONAL environment variables!"
    exit 127
  fi
}

_environment_parse_defaults() {
  log "DEBUG" "ENVIRONMENT > Parsing DEFAULT environment variable values."
  IFS=' ' read -r -a DEFAULTS <<< "${1}"
}

_environment_parse_mandatory() {
  log "DEBUG" "ENVIRONMENT > Parsing MANDATORY environment variables."
  IFS=' ' read -r -a MANDATORY <<< "${1}"
  for VARIABLE in "${MANDATORY[@]}"; do
    if [[ -z ${!VARIABLE} ]]; then
      log "ERROR" "ENVIRONMENT > The environment variable '${VARIABLE}' is required!"
      exit 127
    fi
  done
}

_environment_parse_optional() {
  log "DEBUG" "ENVIRONMENT > Parsing OPTIONAL environment variables."
  IFS=' ' read -r -a OPTIONAL <<< "${1}"
}

_environment_set_defaults() {
  log "DEBUG" "ENVIRONMENT > Setting DEFAULT environment variable values."
  local INDEX=-1
  for VARIABLE in "${DEFAULTS[@]}"; do
    ((INDEX++)) || true
    if [[ -z "${!OPTIONAL[${INDEX}]}" ]]; then
      export "${OPTIONAL[${INDEX}]}"
      eval "${OPTIONAL[${INDEX}]}"="${DEFAULTS[${INDEX}]}"
      log "INFO" "ENVIRONMENT > Default: '${DEFAULTS[${INDEX}]}' is being used for: '${OPTIONAL[${INDEX}]}'."
    fi
  done
}

_environment_usage() {
  log "ERROR" "environment.sh -- require and set defaults for environment variables."
  log "ERROR" "---------------------------------------------------------------------"
  log "ERROR" "environment.sh"
  log "ERROR" "           -d (SPACE SEPARATED LIST OF DEFAULT VALUES FOR OPTIONALS)"
  log "ERROR" "           -o (SPACE SEPARATED LIST OF NAMES FOR OPTIONAL ENV VARS)"
  log "ERROR" "           -m (SPACE SEPARATED LIST OF NAMES FOR MANDATORY ENV VARS)"
  exit 127
}
